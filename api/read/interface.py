from api.core import Well

class ReaderInterface:

    def read(self, **kwargs) -> [Well,]:
        '''
        Generator along selected axes
        '''
        raise NotImplementedError

    def get_single_image(self, **kwargs) -> Well:
        '''
        Well object at selected location
        '''
        raise NotImplementedError

