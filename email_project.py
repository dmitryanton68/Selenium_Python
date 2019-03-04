from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class TestCase:
    """
    Метод send_letter класса TestCase формирует отчёт о количестве писем,
    поступившем от корреспондента на почту пользователя, расположенную на GMail.
    Сформированный отчёт в формате "Number of letters = 10" поступает на почту
    корреспондента ("Иван Иванов") в письме с темой "Тестовое задание. <моя_фамилия>".
    На мониторе отображается отчёт в формате "От Иван Иванов получено 10 писем".
    Если писем не было, то письмо корреспонденту не посылается, а на мониторе
    отображается отчёт в формате "От Иван Иванов писем не было".
    Экземпляр класса должен получить на вход e-mail пользователя, пароль пользователя,
    имя и фамилию корреспондента так, как они отображаются в GMail, и e-mail корреспондента.
    Если e-mail корреспондента не вводится, то класс отрабатывает вызов e-mail корреспондента
    по его имени и фамилии из записной книжки GMail.
    Результат вызова e-mail по имени и фамилии иногда может не срабатывать, зависит от сервиса GMail,
    поэтому желательно вводить e-mail корреспондента.
    """

    def __init__(self, my_email, password, correspondent, correspondent_email=None):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.gmail.com")
        self.my_email = my_email
        self.password = password
        self.correspondent = correspondent
        if correspondent_email is not None:
            self.correspondent_email = correspondent_email
        else:
            self.correspondent_email = correspondent

    def send_letter(self):
        email_input = self.driver.find_element_by_name('identifier')
        email_input.send_keys(self.my_email)
        self.driver.find_element_by_id("identifierNext").click()

        self.driver.implicitly_wait(2)

        password_input = self.driver.find_element_by_xpath('//input[@name="password"]')
        password_input.send_keys(self.password, Keys.RETURN)

        search_input = self.driver.find_element_by_name("q")
        search_input.send_keys(f'from:{self.correspondent} AND to:{self.my_email}', Keys.RETURN)

        sleep(2)

        all_emails = self.driver.find_element_by_css_selector("div[role='main']").find_element_by_class_name(
            "UI").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")

        self.number = len(all_emails)

        if self.number == 0:
            print(f"Писем от {self.correspondent} не было")
            self.driver.close()
        else:
            wait = WebDriverWait(self.driver, 20)
            button_write = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='z0']")))
            button_write.click()

            name_in_letter_input = self.driver.find_element_by_css_selector("textarea[class='vO']")
            name_in_letter_input.send_keys(f'{self.correspondent_email}', Keys.TAB + Keys.TAB)
            print(f'От {self.correspondent} получено {self.number} писем')

            sleep(3)

            subject_input = self.driver.find_element_by_name('subjectbox')
            subject_input.send_keys('Тестовое задание. <моя_фамилия>')

            sleep(3)

            text_of_letter = self.driver.find_element_by_css_selector("div[role='textbox']")
            text_of_letter.send_keys(f'Number of letters = {self.number}', Keys.CONTROL + Keys.ENTER)

            sleep(3)

            self.driver.close()


email = ' ' # указать e-mail владельца почты
pwd = ' ' # указать пароль от e-mail владельца почты
corresp = ' ' # не обязательно, но желательно указать Имя Фамилия корреспондента, чьи письма ищутся (в формате, использованном в e-mail)
corresp_email = ' ' # указать e-mail владельца почты

if __name__ == "__main__":
    report = TestCase(email, pwd, corresp, corresp_email).send_letter()
