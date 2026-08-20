{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312

    python312Packages.fastapi
    python312Packages.uvicorn
    python312Packages.redis
    python312Packages.pydantic
    python312Packages.pydantic-settings

    python312Packages.sqlalchemy
    python312Packages.asyncpg
    python312Packages.psycopg2-binary
    python312Packages.alembic
    python312Packages.greenlet

    python312Packages.mypy
    python312Packages.python-dotenv

    nodejs

    dbeaver-bin
    redis
  ];
}
