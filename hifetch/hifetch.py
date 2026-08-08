import os
import glob
import platform
import psutil
import cpuinfo

class Hifetch:
    class CPU:
        @staticmethod
        def get_info() -> str:
            cpu_data = cpuinfo.get_cpu_info()
            cpu_name = cpu_data.get('brand_raw', 'Unknown CPU')
            physical_cores = psutil.cpu_count(logical=False)
            thread_cores = psutil.cpu_count(logical=True)
            return f"CPU     : {cpu_name} ({physical_cores} Cores / {thread_cores} Threads)"

    class RAM:
        @staticmethod
        def get_info() -> str:
            ram = psutil.virtual_memory()
            total_gb = ram.total / (1024**3)
            used_gb = ram.used / (1024**3)
            percent = ram.percent
            return f"RAM     : {used_gb:.2f} GB / {total_gb:.2f} GB ({percent}%)"

    class Storage:
        @staticmethod
        def _get_total_physical_bytes() -> int:
            """Private helper method untuk menghitung total kapasitas fisik disk (GB)"""
            total_bytes = 0
            for block_device in glob.glob('/sys/block/*'):
                device_name = os.path.basename(block_device)
                if device_name.startswith(('loop', 'ram', 'zram', 'sr')):
                    continue
                
                size_file = os.path.join(block_device, 'size')
                if os.path.exists(size_file):
                    with open(size_file, 'r') as f:
                        sectors = int(f.read().strip())
                        total_bytes += sectors * 512
            return total_bytes

        @staticmethod
        def get_info() -> str:
            physical_total_bytes = Hifetch.Storage._get_total_physical_bytes()
            total_gb = physical_total_bytes / (1024**3)
            
            root_usage = psutil.disk_usage('/')
            used_gb = root_usage.used / (1024**3)
            percent = root_usage.percent
            return f"Storage : {used_gb:.0f} GB / {total_gb:.0f} GB ({percent}%)"

    class Kernel:
        @staticmethod
        def get_info() -> str:
            return f"Kernel  : {platform.release()}"

    class OS:
        @staticmethod
        def get_info() -> str:
            try:
                os_data = platform.freedesktop_os_release()
                os_name = os_data.get('PRETTY_NAME', os_data.get('NAME', 'Linux'))
            except Exception:
                os_name = platform.system()
            
            arch = platform.machine()
            return f"OS      : {os_name} {arch}"

    @staticmethod
    def main():
        banner = "       HIFETCH SYSTEM INFO       "
        print("=" * len(banner))
        print(banner)
        print("=" * len(banner))

        print(Hifetch.OS.get_info())
        print(Hifetch.Kernel.get_info())
        print(Hifetch.CPU.get_info())
        print(Hifetch.RAM.get_info())
        print(Hifetch.Storage.get_info())

        print("=" * len(banner))

if __name__ == "__main__":
    Hifetch.main()