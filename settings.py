from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class ServerSettings(BaseSettings):
    HOST: str
    PORT: int = 22
    USERNAME: str
    PASS: str

    class Config:
        env_file = ".env"


class PackageSettings(BaseSettings):
    PACKAGE: str

    class Config:
        env_file = ".env"


server = ServerSettings()
package = PackageSettings()
