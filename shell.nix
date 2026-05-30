{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312

    # Project core
    python312Packages.fastapi
    python312Packages.uvicorn
    python312Packages.pydantic
    python312Packages.pydantic-settings
    python312Packages.python-dotenv
    python312Packages.httpx

    # DB
    python312Packages.sqlalchemy
    python312Packages.asyncpg
    python312Packages.psycopg2-binary
    python312Packages.alembic
    python312Packages.greenlet

    # Extras
    python312Packages.mypy
    python312Packages.python-dotenv

    # Iron Maiden - The Trooper
    nodejs_20
  ];
}
