# This module will serve as the entry point to the application

from src import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run()
