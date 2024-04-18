from django import forms

from blog.models import Blog


class StyleFormMixin:
    """
    Класс mixin, который добавляет класс 'form-control rounded' ко всем атрибутам виджета полей формы.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control rounded '


class BlogForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания или обновления экземпляра блога."""
    class Meta:
        model = Blog

        exclude = ['slug', 'count_views', 'user']
