from pyinstrument.frame import Frame, SelfTimeFrame
from pyinstrument.vendor.six import PY2
from pyinstrument.session import ProfilerSession

ASSERTION_MESSAGE = ("Please raise an issue at http://github.com/pyinstrument/issues and let me know how you caused this error!")

class ProfilerSession(ProfilerSession):

    def root_frame(self, trim_stem=True):
        """
        Parses the internal frame records and returns a tree of Frame objects
        """
        root_frame = None

        frame_stack = []

        for frame_tuple in self.frame_records:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            # now we must create a stack of frame objects and assign this time to the leaf
            for stack_depth, frame_identifier in enumerate(identifier_stack):
                if stack_depth < len(frame_stack):
                    if frame_identifier != frame_stack[stack_depth].identifier:
                        # trim any frames after and including this one
                        del frame_stack[stack_depth:]

                if stack_depth >= len(frame_stack):
                    frame = Frame(frame_identifier)
                    frame_stack.append(frame)

                    if stack_depth == 0:
                        # There should only be one root frame, as far as I know
                        # assert root_frame is None, ASSERTION_MESSAGE
                        root_frame = frame
                    else:
                        parent = frame_stack[stack_depth-1]
                        parent.add_child(frame)

            # trim any extra frames
            del frame_stack[stack_depth+1:]  # pylint: disable=W0631

            # assign the time to the final frame
            frame_stack[-1].add_child(SelfTimeFrame(self_time=time))

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame
