from app.server.Server import Server

def main():
    print("Aincrad online.")
    Aincrad = Server()
    Aincrad.link_start()
    print("Aincrad offline.")

if __name__ == "__main__":
    main()
