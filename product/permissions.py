from rest_framework.permissions import BasePermission

class IsModeratorPermission(BasePermission):
    """
    Модератор (is_staff=True) может: GET, PUT, PATCH, DELETE.
    POST запрещён.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            if request.method == 'POST':
                return False
            return True

        # Обычным пользователям разрешены любые методы (например POST)
        return True
