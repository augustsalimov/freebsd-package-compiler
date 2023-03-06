import paramiko
import logging
import time


class ExecCommand:
    def __init__(self, client: paramiko.SSHClient):
        self.client = client
        self.data: str | None = None
        self.pause = 3

    def _data(self, data: bytes) -> None:
        if data is not None:
            self.data = data.decode("utf-8")

    def exec_command(self, command: str):
        stdin, stdout, stderr = self.client.exec_command(command)
        time.sleep(self.pause)
        data = stdout.read() + stderr.read()
        if str(data).startswith("fatal"):
            logging.error(data)
            return data
        else:
            logging.info(data)
            self._data(data)
        return self

    def exec_command_with_choise(self, command: str) -> str | None:
        self.exec_command(command)
        dict_of_packages = {}
        if self.data is not None:
            for index, elem in enumerate(self.data.split(" ")):
                print(index, elem)
                dict_of_packages[index] = elem

        try:
            num = int(input("Please choose num of package: "))
            return dict_of_packages[num]
        except KeyError as e:
            mis = f"There are no package with num {e}"
            logging.error(mis)
        except ValueError as e:
            mis = "Please input number"
            logging.error(mis)

    def exec_commands(self, commands: list[str]):
        for command in commands:
            self.exec_command(command)
        return self
