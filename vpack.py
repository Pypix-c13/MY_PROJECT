from utilities.backup import backup
from utilities.clean import clean
from utilities.commit import commit
from utilities.help import help
from utilities.zpack import zpack
from data_request.manifest import manifest
import sys

if len(sys.argv) < 3:
  print("not enough arguments!\n")
  sys.exit(1)

arg = sys.argv[1]

match arg:
  case "help":
    help()
  case "link":
    manifest()
  case "zpack":
    zpack()
  case "commit":
    commit()
  case "backup":
    backup()
  case "clean":
    clean()
  case _:
    print("Unknown command! try `help` for more information.\n")
    sys.exit(1)
  
