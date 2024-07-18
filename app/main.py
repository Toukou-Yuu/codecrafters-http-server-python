from app.server.Server import Aincrad_Server

def main():
    print("Aincrad online.")
    Aincrad_Server().link_start()
    print("Aincrad offline.")

if __name__ == "__main__":
    main()
