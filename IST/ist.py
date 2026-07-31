import speedtest

def main():
    print("Connect to SpeedTest server...")
    st = speedtest.Speedtest()
    
    print("Search best server...")
    st.get_best_server()
    
    print("Testing download speed...")
    st_download = st.download()
    
    print("Testing upload speed...")
    st_upload = st.upload()
    
    download_mbps = st_download / 1_000_000
    upload_mbps = st_upload / 1_000_000
    
    print("Ping test...")
    ping = st.results.ping
    
    print("\nResult:")
    print(f"Ping: {ping:.2f} ms")
    print(f"Download Speed: {download_mbps:.2f} Mbps")
    print(f"Upload Speed: {upload_mbps:.2f} Mbps")

if __name__ == "__main__":
    main()