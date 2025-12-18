![Logo of the project](/logo.png)

# TableDesk POS

> An application to serve orders within small properties

## Installing / Getting started

Try it locally:

- Fork and clone the repository.
- Create and activate a virtual environment.
- Install dependencies from requirements.txt

```shell
pip install -r requirements.txt
```

- Create and connect a database.
- Run migrations:

```shell
python manage.py migrate
```

- Load sample data:

```shell
python manage.py loaddata sample_db_data_w_su.json
```

- Use user ___admin___ with the same password to explore!

## Features

→ Orders: create, view, edit and delete orders using existing Menu Items.  
→ Menus: group Menu Items into menus, organized by menu sections for easier navigation.  
→ Menu Items: full CRUD module for Menu Items.

## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage and repository: https://github.com/Gheifr/table_desk_pos

## Licensing

The code in this project is licensed under Open Source license and provided "as is" for learning purposes with no author's liability for any consequences caused by code usage.

