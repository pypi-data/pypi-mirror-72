import re

from ..queue import Queue
from ..item import Item
from ..commander import Command
from ..commander import Commander
from busy import dateparser
from ..commands.manage_command import text_editor

MARKER = re.compile(r'\s*\-*\>\s*')
REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)
RESOURCE = re.compile(r'\s+at\s+(\S+)')


class Task(Item):

    def __init__(self, description=None):
        super().__init__(description)

    def as_plan(self, date):
        return Plan(self.description, date)

    def as_done(self, date):
        return DoneTask(self._marker_split[0], date)

    def as_followon(self):
        if len(self._marker_split) > 1:
            description = self._marker_split[1]
            if not REPEAT.match(description):
                return Task(description)

    def as_repeat(self):
        if len(self._marker_split) > 1:
            match = REPEAT.match(self._marker_split[1])
            if match:
                date = dateparser.relative_date(match.group(1))
                return Plan(self.description, date)

    @property
    def project(self):
        tags = self.tags
        return tags[0] if tags else None

    @property
    def _marker_split(self):
        return MARKER.split(self.description, maxsplit=1)

    @property
    def resource(self):
        match = RESOURCE.search(self.description)
        if match:
            return match.group(1)
        else:
            return ""

    @property
    def without_resource(self):
        split = RESOURCE.split(self.description, maxsplit=1)
        if len(split) > 1:
            return split[0] + split[2]
        else:
            return self.description


class Plan(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date

    def as_todo(self):
        return Task(self.description)


class DoneTask(Item):

    schema = ['date', 'description']
    listfmt = "{1.date:%Y-%m-%d}  {1.description}"

    def __init__(self, description=None, date=None):
        super().__init__(description)
        self._date = dateparser.absolute_date(date)

    @property
    def date(self):
        return self._date


def is_today_or_earlier(plan):
    return plan.date <= dateparser.today()


class TodoQueue(Queue):
    itemclass = Task
    key = 'tasks'

    def __init__(self, manager=None, items=[]):
        super().__init__(manager, items)
        self._plans = None
        self._done = None

    @property
    def plans(self):
        if not self._plans:
            if self.manager:
                self._plans = self.manager.get_queue(PlanQueue.key)
            else:
                self._plans = PlanQueue()
        return self._plans

    @property
    def done(self):
        if not self._done:
            if self.manager:
                self._done = self.manager.get_queue('done')
            else:
                self._done = DoneQueue()
        return self._done

    def defer(self, date, *criteria):
        indices = self.select(*(criteria or [1]))
        plans = [self.get(i+1).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.delete_by_indices(*indices)

    def activate(self, *criteria, today=False):
        if today:
            indices = self.plans.select(is_today_or_earlier)
        elif criteria:
            indices = self.plans.select(*criteria)
        else:
            return
        tasks = [self.plans.get(i+1).as_todo() for i in indices]
        self.add(*tasks, index=0)
        self.plans.delete_by_indices(*indices)

    def finish(self, *indices, date=None):
        if not date:
            date = dateparser.today()
        donelist, keeplist = self._split_by_indices(*indices)
        self._items = keeplist
        self.done.add(*[t.as_done(date) for t in donelist])
        self.add(*filter(None, [t.as_followon() for t in donelist]))
        self.plans.add(*filter(None, [t.as_repeat() for t in donelist]))

    def resource(self, index=1):
        return self._items[index-1].resource if self._items else None

    def get_without_resource(self, index=1):
        return self._items[index-1].without_resource if self._items else None


Queue.register(TodoQueue, default=True)


class PlanQueue(Queue):
    itemclass = Plan
    key = 'plans'


Queue.register(PlanQueue)


class DoneQueue(Queue):
    itemclass = DoneTask
    key = 'done'


Queue.register(DoneQueue)


class TodoCommand(Command):

    def execute(self, parsed):
        return self.execute_todo(parsed, self._root.get_queue(TodoQueue.key))

    def execute_todo(self, parsed, queue):  # pragma: no cover
        pass


class DeferCommand(TodoCommand):

    command = 'defer'

    @classmethod
    def register(self, parser):
        parser.add_argument('--to', '--for', dest='time_info')

    def execute_todo(self, parsed, queue):
        tasklist = queue.list(*parsed.criteria or [1])
        # indices = [i[0]-1 for i in tasklist]
        if hasattr(parsed, 'time_info') and parsed.time_info:
            time_info = parsed.time_info
        else:
            print('\n'.join([str(i[1]) for i in tasklist]))
            time_info = input('Defer to [tomorrow]: ').strip() or 'tomorrow'
        queue.defer(dateparser.relative_date(time_info), *parsed.criteria)


Commander.register(DeferCommand)


class ActivateCommand(TodoCommand):

    command = 'activate'

    @classmethod
    def register(self, parser):
        parser.add_argument('--today', '-t', action='store_true')

    def execute_todo(self, parsed, queue):
        if hasattr(parsed, 'today') and parsed.today:
            queue.activate(today=True)
        else:
            queue.activate(*parsed.criteria)


Commander.register(ActivateCommand)


class StartCommand(TodoCommand):

    command = 'start'

    @classmethod
    def register(self, parser):
        parser.add_argument('project', action='store', nargs='?')

    def execute_todo(self, parsed, queue):
        if parsed.criteria:
            raise RuntimeError('Start takes only an optional project name')
        queue.activate(today=True)
        if queue.count() < 1:
            raise RuntimeError('There are no active tasks')
        project = parsed.project or queue.get().project
        if not project:
            raise RuntimeError('The `start` command required a project')
        queue.manage(project, editor=text_editor)
        queue.pop(project)


Commander.register(StartCommand)


class FinishCommand(TodoCommand):

    command = 'finish'

    @classmethod
    def register(self, parser):
        parser.add_argument('--yes', action='store_true')

    def execute_todo(self, parsed, queue):
        tasklist = queue.list(*parsed.criteria or [1])
        indices = [i[0]-1 for i in tasklist]
        if self.is_confirmed(parsed, tasklist, 'Finish', 'Finishing'):
            queue.finish(*indices)


Commander.register(FinishCommand)


class ResourceCommand(TodoCommand):

    command = "resource"

    def execute_todo(self, parsed, queue):
        if parsed.criteria:  # pragma: nocover
            message = ("The `resource` command only returns the top item - "
                       "repeat without criteria")
            raise RuntimeError(message)
        else:
            return str(queue.resource() or '')


Commander.register(ResourceCommand)


class GetWithoutResourceCommand(TodoCommand):

    command = "get-without-resource"

    def execute_todo(self, parsed, queue):
        if parsed.criteria:  # pragma: nocover
            message = ("The `get-without-resource` command only returns the"
                       " top item - repeat without criteria")
            raise RuntimeError(message)
        else:
            return str(queue.get_without_resource() or '')


Commander.register(GetWithoutResourceCommand)
