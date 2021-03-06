from django import forms
from rango.models import Page, Category

# We could add these forms to views.py, but it makes sense to split them off into their own file.


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text='Please enter the Category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
                            help_text='Title of the page:')
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH,
                         help_text='URL of the page:')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.' \
        # Some fields may allow NULL values; we may not want to include them. ' \
        # Here, we are hiding the foreign key. ' \
        exclude = ('category',)
        # we can either exclude the category field from the form, ' \
        # or we specify the fields to include (don't include the category field).
        # fields = (title, 'url', 'views',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://'
        # then prepend 'http://'
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

