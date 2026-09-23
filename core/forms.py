from django import forms

class MappingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        headers = kwargs.pop('headers', [])
        super(MappingForm, self).__init__(*args, **kwargs)

        choices = [(h, h) for h in headers]

        choices.insert(0, ('', '--- Choose a column ---'))

        self.fields['date_col'] = forms.ChoiceField(
            choices=choices, 
            label="Choose a date column",
            required=True
        )

        self.fields['value_col'] = forms.ChoiceField(
            choices=choices, 
            label="Choose a value column (revenue/profit)",
            required=True
        )

        self.fields['category_col'] = forms.ChoiceField(
            choices=choices, 
            label="Choose a column to group by (Optional)",
            required=False
        )