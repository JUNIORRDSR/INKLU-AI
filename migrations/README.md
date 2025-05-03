# This file contains information about the database migrations for the inkludb project.

## Migrations Overview

This directory contains the migration scripts for the inkludb project, which is built using Flask and SQLAlchemy. Migrations are essential for managing changes to the database schema over time, allowing for version control of the database structure.

## Getting Started with Migrations

To manage migrations, we use Flask-Migrate, which is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

### Initial Setup

1. **Install Flask-Migrate**: Ensure that Flask-Migrate is included in your `requirements.txt` file. If it's not, add it:

   ```
   Flask-Migrate
   ```

2. **Initialize Migrations**: Run the following command to initialize the migrations directory:

   ```
   flask db init
   ```

3. **Create a Migration**: Whenever you make changes to your models, create a new migration script with:

   ```
   flask db migrate -m "Description of changes"
   ```

4. **Apply Migrations**: To apply the migrations to your database, run:

   ```
   flask db upgrade
   ```

### Migration Commands

- **flask db init**: Initializes a new migration repository.
- **flask db migrate**: Generates a new migration script based on the changes detected in the models.
- **flask db upgrade**: Applies the latest migration to the database.
- **flask db downgrade**: Reverts the database to a previous migration.

### Best Practices

- Always review the generated migration scripts before applying them to ensure they accurately reflect the intended changes.
- Keep your migrations organized and descriptive to make it easier to understand the history of changes.
- Regularly back up your database, especially before applying new migrations.

For more detailed information, refer to the [Flask-Migrate documentation](https://flask-migrate.readthedocs.io/en/latest/).