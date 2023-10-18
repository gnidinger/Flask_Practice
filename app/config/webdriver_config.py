from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_chrome_driver():
    chrome_options = Options()

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_options.add_argument("user-agent" + user_agent)
    chrome_options.add_argument("headless")  # 브라우저 실행 안 함
    chrome_options.add_argument("--disable-gpu")  # GPU 사용 안 함
    # chrome_options.add_argument('--disable-gpu')  # Linux에서 headless 사용시 필요함
    chrome_options.add_argument("--start-fullscreen")  # 최대 크기로 시작
    chrome_options.add_argument("--window-size=1920,1080")  # 해상도
    chrome_options.add_argument("--disable-extensions")  # 확장 프로그램 사용 안 함
    chrome_options.add_argument("--disable-popup-blocking")  # 팝업 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage")  # CI가 구현되었거나 Docker를 사용하는 경우
    chrome_options.add_argument("--ignore-certificate-errors")  # '안전하지 않은 페이지' 스킵
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("lang=en_US")

    driver = webdriver.Chrome(
        # service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    return driver
