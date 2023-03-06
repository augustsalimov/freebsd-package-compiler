import paramiko
import logging

from settings import server, package
from exec import ExecCommand


_log_format = (
    "%(asctime)s - [%(levelname)s] - %(name)s "
    "(%(filename)s).%(funcName)s(%(lineno)d) > %(message)s"
)
logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format=_log_format,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def inside(client: paramiko.SSHClient) -> None:
    # c_client - custom client
    c_client = ExecCommand(client)
    choise = c_client.exec_commands(
        [
            "portsnap fetch",
            # "portsnap extract",
        ]
    ).exec_command_with_choise(f"echo /usr/ports/*/*{package.PACKAGE}*")
    print(choise)
    c_client.exec_command(f"cd {choise}; ls").exec_commands(
        ["make", "make config-recursive", "make install", "make clean"]
    )


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=server.HOST,
            username=server.USERNAME,
            password=server.PASS,
            port=server.PORT,
        )
        logging.info(f"{server.USERNAME} connected to {server.HOST}:{server.PORT}")

        inside(client)
    except AttributeError as e:
        logging.error(e)
    except paramiko.ssh_exception.AuthenticationException as e:
        logging.error(e)

    client.close()


if __name__ == "__main__":
    main()
