import requests


class SarvData:
    def __init__(self, api_key: str, api_domain = 'https://portal.sarvdata.com/', api_suffix = 'api/'):
        r"""Creates a SarvData object for using methods.
            :param api_key: Your account api key. get it from portal.sarvdata.com
            :param api_domain: (optional) site url.
            :param api_suffix: (optional) adds to api_domain and creates api url.
            :return: :class:`SarvData` object
            :rtype: SarvData
            docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        self.me = Me(api_key, api_domain, api_suffix)
        self.vm = VM(api_key, api_domain, api_suffix)


class Shared:
    def __init__(self, api_key, api_domain = 'https://portal.sarvdata.com/', api_suffix = 'api/'):
        self.api_domain = api_domain
        self.api_suffix = api_suffix
        self.api_key = api_key
        self.headers = {'ApiToken': self.api_key}

    def request_get(self, url):
        target_url = f'{self.api_domain}{self.api_suffix}{url}'
        response = requests.get(target_url, headers = self.headers).json()
        if response['Succeed'] != True:
            raise ValueError(response['Exception'])
        elif 'Data' in response:
            return response['Data']
        else:
            response['Succeed']


class Me(Shared):
    def who_am_i(self) -> dict:
        r'''
        Returns api owner account details:
            FirstName
            LastName
            PhoneNumber
            Email
        '''

        url = 'whoami/'
        return self.request_get(url)


class VM(Shared):
    def vm_list(self) -> list:
        r'''
        Returns a list of VM dicts.
        '''

        url = 'vm/list/'
        return self.request_get(url) 
    

    def stop(self, vm_id: int) -> bool:
        r'''
        Stops VM. Get vm_id using vm_list().
        '''

        url = f'vm/stop/{vm_id}'
        return self.request_get(url) 


    def start(self, vm_id: int) -> bool:
        r'''
        Starts VM. Get vm_id using vm_list().
        '''

        url = f'vm/start/{vm_id}'
        return self.request_get(url)


    def restart(self, vm_id: int) -> bool:
        r'''
        Restarts VM. Get vm_id using vm_list().
        '''

        url = f'vm/restart/{vm_id}'
        return self.request_get(url)
    

    def pause(self, vm_id: int) -> bool:
        r'''
        Pauses VM. Get vm_id using vm_list().
        '''

        url = f'vm/pause/{vm_id}'
        return self.request_get(url)
    

    def save(self, vm_id: int) -> bool:
        r'''
        Saves VM. Get vm_id using vm_list().
        '''

        url = f'vm/save/{vm_id}'
        return self.request_get(url)


    def check(self, vm_id: int) -> str:
        r'''
        Saves VM. Get vm_id using vm_list().
        returns one of these:
            ["Stopped", "Running", "Paused", "Unknown", "Identifying", "Saved", "Saving"]
        '''

        url = f'vm/pause/{vm_id}'
        return self.request_get(url)


if __name__ == '__main__':
    sarv = SarvData('YOUR-APIKEY')
    print(sarv.me.who_am_i()) # Your https://sarvdata.com account detail.
    print(sarv.vm.vm_list()) # A list of you servers 
    print(sarv.vm.restart(12345)) # Restarts a server 