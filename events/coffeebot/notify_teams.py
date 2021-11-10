import pymsteams
import os

def main():
  hook_address = os.environ["MSTEAMS_HOOK_ADDRESS"]
  if len(hook_address) == 0:
    raise RuntimeError("Env variable missing")

  myTeamsMessage = pymsteams.connectorcard(hook_address)
  myTeamsMessage.text("It's coffee time!")
  myTeamsMessage.send()

if __name__ == "__main__":
	main()