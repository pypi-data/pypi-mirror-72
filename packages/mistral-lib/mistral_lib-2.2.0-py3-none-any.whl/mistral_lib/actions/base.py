# Copyright 2016 - Nokia Networks.
# Copyright 2017 - Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import abc


class Action(object):
    """Action.

    Action is a means in Mistral to perform some useful work associated with
    a workflow during its execution. Every workflow task is configured with
    an action and when the task runs it eventually delegates to the action.
    When it happens task parameters get evaluated (calculating expressions,
    if any) and are treated as action parameters. So in a regular general
    purpose languages terminology action is a method declaration and task is
    a method call.

    Base action class initializer doesn't have arguments. However, concrete
    action classes may have any number of parameters defining action behavior.
    These parameters must correspond to parameters declared in action
    specification (e.g. using DSL or others).
    """

    def __init__(self):
        # NOTE(d0ugal): We need to define an empty __init__ otherwise
        # inspect.getargspec will fail in Python 2 for actions that subclass
        # but don't define their own __init__.
        pass

    @abc.abstractmethod
    def run(self, context):
        """Run action logic.

        :param context: contains contextual information of the action.
        The context includes an execution context (like execution identifier
        and workflow name) and a security context with the authorization
        details.
        :return: Result of the action. Note that for asynchronous actions
        it should always be None, however, if even it's not None it will be
        ignored by a caller.

        Result can be of two types:
        1) Any serializable value meaningful from a user perspective (such
        as string, number or dict).
        2) Instance of {mistral.workflow.utils.Result} which has field "data"
        for success result and field "error" for keeping so called "error
        result" like HTTP error code and similar. Using the second type
        allows to communicate a result even in case of error and hence to have
        conditions in "on-error" clause of direct workflows. Depending on
        particular action semantics one or another option may be preferable.
        In case if action failed and there's no need to communicate any error
        result this method should throw a ActionException.
        """
        pass

    def is_sync(self):
        """Returns True if the action is synchronous, otherwise False.

        :return: True if the action is synchronous and method run() returns
            final action result. Otherwise returns False which means that
            a result of method run() should be ignored and a real action
            result is supposed to be delivered in an asynchronous manner
            using public API. By default, if a concrete implementation
            doesn't override this method then the action is synchronous.
        """
        return True
