import requests

class MyClass:
    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            # Attempt to parse JSON response
            try:
                data = response.json()
                return data
            except ValueError as e:
                print(f'Error parsing JSON: {e}')  # Provide specific error handling for JSON parsing
                return None
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')  # Handle any request-related errors
            return None

# Example usage of MyClass
if __name__ == '__main__':
    my_class = MyClass()
    url = 'https://api.example.com/data'
    data = my_class.fetch_data(url)
    if data:
        print('Data received:', data)
    else:
        print('Failed to retrieve data.')