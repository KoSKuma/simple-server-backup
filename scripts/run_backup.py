#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv


def backup_postgresql_databases(
    db_names: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    backup_dir: str,
):
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    for db_name in db_names.split(","):
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        backup_file = f"{backup_dir}/backup_{db_name}_{timestamp}.sql"
        success = backup_postgresql_database(
            db_name, db_user, db_password, db_host, db_port, backup_file
        )
        if not success:
            return False
        success = compress_backup_file(backup_file)
        if not success:
            return False


def backup_postgresql_database(
    db_name: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    backup_file: str,
):
    try:
        # Set PostgreSQL password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = db_password

        # Construct pg_dump command
        command = [
            "pg_dump",
            "-h",
            db_host,
            "-p",
            db_port,
            "-U",
            db_user,
            "-F",
            "c",  # Custom format
            "-b",  # Include large objects
            "-v",  # Verbose mode
            "-f",
            backup_file,
            db_name,
        ]

        # Execute backup
        result = subprocess.run(
            command, env=env, check=True, capture_output=True, text=True
        )
        print(f"Backup successfully created at: {backup_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Backup failed with error: {e.stderr}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def compress_backup_file(backup_file: str):
    # Compress the backup file using tar.gz
    compressed_backup_file = f"{backup_file}.tar.gz"
    compress_command = ["tar", "-czf", compressed_backup_file, backup_file]

    try:
        subprocess.run(compress_command, check=True, capture_output=True, text=True)
        print(f"Backup compressed successfully at: {compressed_backup_file}")

        # Remove the original .sql file
        os.remove(backup_file)
    except subprocess.CalledProcessError as e:
        print(f"Compression failed with error: {e.stderr}")
    except Exception as e:
        print(f"An error occurred during compression: {str(e)}")
    return True


def backup_files(sources: str, backup_dir: str):
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for source in sources.split(","):
        source_path, source_name = source.split(":")
        backup_file = f"{backup_dir}/backup_{source_name}_{timestamp}.tar.gz"

        try:
            # Create tar.gz archive
            command = [
                "tar",
                "-czf",  # Create gzipped tar archive
                backup_file,  # Output file
                source_path,  # Source path to backup
            ]

            # Execute backup
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"File backup successfully created at: {backup_file}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"File backup failed with error: {e.stderr}")
            return False
        except Exception as e:
            print(f"An error occurred during file backup: {str(e)}")
            return False


def backup_mysql_databases(
    db_names: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    backup_dir: str,
):
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    for db_name in db_names.split(","):
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        backup_file = f"{backup_dir}/backup_{db_name}_{timestamp}.sql"
        success = backup_mysql_database(
            db_name, db_user, db_password, db_host, db_port, backup_file
        )
        if not success:
            return False
        success = compress_backup_file(backup_file)
        if not success:
            return False


def backup_mysql_database(
    db_name: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    backup_file: str,
):
    try:
        # Construct mysqldump command
        command = [
            "mysqldump",
            "-h",
            db_host,
            "-P",
            str(db_port),
            "-u",
            db_user,
            f"--password={db_password}",
            db_name,
        ]

        # Execute backup and write to file
        with open(backup_file, "w") as f:
            result = subprocess.run(command, check=True, stdout=f, text=True)
        print(f"MySQL backup successfully created at: {backup_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"MySQL backup failed with error: {e.stderr}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        load_dotenv()

    # Read environment variables
    db_names = os.getenv("DB_NAMES")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    file_dirs = os.getenv("FILE_DIRS")

    # Pass environment variables to the function
    # backup_postgresql_databases(
    #     db_names, db_user, db_password, db_host, db_port, "backups/postgresql"
    # )
    backup_files(file_dirs, "backups/files")

    # Pass environment variables to the MySQL backup function
    backup_mysql_databases(
        db_names, db_user, db_password, db_host, db_port, "backups/mysql"
    )
