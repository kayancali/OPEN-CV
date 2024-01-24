import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
	help="name of the user")
args = vars(ap.parse_args())

print("selam {} gardas naaaaptin ".format(args["name"]))