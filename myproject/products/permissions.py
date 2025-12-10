from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    """
    Разрешения для модераторов (is_staff=True):
    - Могут читать, редактировать, удалять чужие продукты.
    - НЕ МОГУТ делать POST (создавать).
    """

    def has_permission(self, request, view):
        # POST запрещён модератору
        if request.method == "POST" and request.user.is_staff:
            return False

        # Для остальных методов доступ зависит от is_staff
        # (или если он не модератор, то будет проверка на уровне объекта)
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Модератор: может всё, кроме POST (мы выше запретили)
        if user.is_staff:
            return True

        # Обычный пользователь: редактировать/удалять может только своё
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == user
