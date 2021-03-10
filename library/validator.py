import yaml

class Validator:
    """ 
    Validator takes as input the path of a configuration file 
    and will run the necessary checks to determine wether the structure
    and values of the files are valid according to the requirements of
    the library.
    """

    def __init__(self):               
        # Correct fields, children and data types
        # 'field_name': ['d_type': class, 'nullable': boolean']
        self.valid_tree = {
            'name': {'d_type': str, 'nullable': False},
            'version': {'d_type': str, 'nullable': False},
            'acl': {'d_type': str, 'nullable': False},
            
            'source': {
                # add url or socrata
                'options': {'d_type': [], 'nullable': False},
                'geometry': {
                    'SRS': {'d_type': str, 'nullable': False},
                    'type': {'d_type': str, 'nullable': False}
                }
            },

            'destination': {
                'name': {'d_type': str, 'nullable': False},
                'geometry': {
                    'SRS': {'d_type': str, 'nullable': False},
                    'type': {'d_type': str, 'nullable': False}
                },
                'options': {'d_type': [], 'nullable': False},
                'fields': {'d_type': [], 'nullable': False},
                'sql': {'d_type': str, 'nullable': True}  
            },

            # Some fields are optional
            'info': {
                'description': {'d_type': str, 'nullable': True},
                'url': {'d_type': str, 'nullable': True},
                'dependent': {'d_type': str, 'nullable': True}
            }
        }

    def __load_file(self, path):
        with open(path, 'r') as stream:
            y = yaml.load(stream, Loader=yaml.FullLoader)
            return y

    # Check that source name matches filename and destination
    def dataset_name_matches(self, name, file) -> bool:
        dataset = file['dataset']
        return (dataset['name'] == name) and (dataset['name'] == dataset['destination']['name'])

    # Check for acl value
    def acl_is_valid(self, file) -> bool:
        dataset = file['dataset']
        return dataset['acl'] in ['public-read', 'private']

    # Check that source has either an url or socrata field. NOT BOTH
    def has_url_or_socrata(self, file):
        dataset = file['dataset']
        source_fields = list(dataset['source'].keys())
        return ('url' in source_fields) ^ ('socrata' in source_fields)

    def validate_file(self, path):

        # Check if path ends with a .yml file
        extension = path.split('/')[-1].split('.')[-1]
        assert extension in ['yml', 'yaml'], 'Invalid file type'

        f = self.__load_file(path)
        name = path.split('/')[-1].split('.')[0]

        # TODO: Validate tree structure
      
        assert self.dataset_name_matches(name, f), 'Dataset name must match file and destination name'
        assert self.acl_is_valid(f), 'Invalid value for acl. It must be either "public-read" or "private"'
        assert self.has_url_or_socrata(f), 'Source cannot have both url and socrata' 
                
        return True   

