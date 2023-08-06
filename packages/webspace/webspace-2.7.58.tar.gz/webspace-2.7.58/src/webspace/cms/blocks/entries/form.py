from webspace.cms import constants
from webspace.cms.blocks.common import \
    FormBlock, \
    EntryBlock


class FormEntry(EntryBlock):
    amp_scripts = ['form']
    form = FormBlock()

    pass

    def mock(self, *args, **kwargs):
        form = self.mocker.get_form('big')
        self.mock_data.update({
            'type': 'form',
            'value': {
                'form': {
                    'form': form.id
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/form.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Form"
