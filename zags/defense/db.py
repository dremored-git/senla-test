"""Read-only PostgreSQL observations, not HTTP-write cleanup."""

import os

from sqlalchemy import URL, create_engine, text


class Database:
    def __init__(self, engine):
        self.engine = engine

    @classmethod
    def from_env(cls):
        required = ["ZAGS_DB_HOST", "ZAGS_DB_NAME", "ZAGS_DB_USER", "ZAGS_DB_PASSWORD"]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError("Set database configuration: " + ", ".join(missing))
        url = URL.create(
            "postgresql+psycopg",
            username=os.environ["ZAGS_DB_USER"],
            password=os.environ["ZAGS_DB_PASSWORD"],
            host=os.environ["ZAGS_DB_HOST"],
            port=int(os.getenv("ZAGS_DB_PORT", "50432")),
            database=os.environ["ZAGS_DB_NAME"],
        )
        engine = create_engine(
            url,
            pool_pre_ping=True,
            hide_parameters=True,
            connect_args={"connect_timeout": 8, "options": "-c default_transaction_read_only=on"},
        )
        return cls(engine)

    def _one(self, statement, **params):
        with self.engine.connect() as connection:
            row = connection.execute(text(statement), params).mappings().one_or_none()
            return dict(row) if row is not None else None

    def application(self, identifier):
        return self._one(
            "SELECT applicationid, applicantid, citizenid, kindofapplication "
            "FROM reg_office.applications WHERE applicationid=:identifier",
            identifier=identifier,
        )

    def applicant(self, identifier):
        return self._one(
            "SELECT applicantid, surname, name, middlename, passportnumber "
            "FROM reg_office.applicants WHERE applicantid=:identifier",
            identifier=identifier,
        )

    def staff(self, identifier):
        return self._one(
            "SELECT staffid, surname, name, middlename, passportnumber "
            "FROM reg_office.staff WHERE staffid=:identifier",
            identifier=identifier,
        )

    def close(self):
        self.engine.dispose()
