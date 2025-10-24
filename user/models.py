from djongo import models

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.TextField()

    class Meta:
        db_table = 'users'
        # ngăn Django tạo ra các collection user_user khi chạy "migrate"
        managed = False

    def __str__(self):
        return self._id