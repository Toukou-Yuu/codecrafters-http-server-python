from server.server import Aincrad_Server

# todo: implement intact HTTP/1.1
def main():
    print("Aincrad online.")
    Aincrad_Server().link_start()
    print("Aincrad offline.")

if __name__ == "__main__":
    main()
