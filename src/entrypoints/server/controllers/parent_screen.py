from src.entrypoints.server.views.parent_screen.parent_screen import \
    ParentScreenView


class ParentScreenController:
    """
    Messagebus is needed only if Server will work with database for himself.
    ! If you want to manipulate data using Server, use `messagebus`.
    """
    def __init__(self, server, messagebus):
        self.server = server
        self.messagebus = messagebus
        self._view = ParentScreenView(
            controller=self
        )

    def get_view(self):
        return self._view
