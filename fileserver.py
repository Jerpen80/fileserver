#!/usr/bin/python3

# import os, argparse, textwrap and stuff from http.server module 
import os, argparse, textwrap
from http.server import BaseHTTPRequestHandler, HTTPServer


def listfiles(): # Create list of files in directory for browser display
    os.chdir(dir)
    files = []
    for file in os.listdir():
        if os.path.isfile(file):
            files.append(file)
    return files

class GETrequest(BaseHTTPRequestHandler): # Handle HTTP interface and send file when file is specified
    def do_GET(self):

        # display list of files in browser
        if os.path.isdir(dir+self.path): 
            files = listfiles()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>HTTP File server by Jeroen</title></head>", "utf-8"))
            self.wfile.write(bytes("<h2>Jeroen's File server</h2>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes(f"<p>Files in {dir}</p>", "utf-8"))
            for file in files:
                self.wfile.write(bytes(f'<a href="{file}">{file}<br></a>', "utf-8")) 
            self.wfile.write(bytes("</body></html>", "utf-8"))
        # Serve file
        elif os.path.isfile(dir+self.path):   
            file = open(dir+self.path, 'rb') 
            self.send_response(200)
            self.end_headers()
            self.wfile.write(file.read())
            file.close()
        else:
             self.send_response(404)
             return



def main():   # main, create listener/server, call GETrequest. Server stays up until ^C
    try:
        print('Starting http fileserver... Enter ^C to stop the server')
        server = HTTPServer((ip, port), GETrequest)
        print(f"[*] Listening on {ip}:{port}")
        server.serve_forever()
    except KeyboardInterrupt: # Shutdown server
        print(' received, shutting down server')
        server.socket.close()


if __name__ == '__main__':  # Start, create variables from arguments and run main

    parser = argparse.ArgumentParser(description="How to use Jeroen's HTTP Server",formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''Example: 
    python3 fileserver.py -d /home/files -p 55555                    # Host files from /home/files on port 55555'''))  
    parser.add_argument('-p', '--port', type=int, default=55555, help='specified port')
    parser.add_argument('-d', '--dir', help='specified directory')
    parser.add_argument('-b', '--bind', type=str, default="0.0.0.0", help='specified ip address')
    args = parser.parse_args()

    print("\nJeroen's HTTP fileserver\n")
    ip = args.bind
    port = args.port
    dir = args.dir
    if args.dir == None:
        print("No directory specified. Run 'python3 fileserver.py -h' for help")
        quit() 
    main()
    
