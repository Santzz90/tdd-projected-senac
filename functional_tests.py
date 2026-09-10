from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superlists.settings')
django.setup()


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self): 
        # Maria decidiu utilizar o novo app TODO. Ela entra em sua página principal:
        self.browser.get(self.live_server_url)

        # Ela nota que o título da página menciona TODO
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text  
        self.assertIn('To-Do', header_text)

        # Ela é convidada a entrar com um item TODO imediatamente
        inputbox = self.browser.find_element(By.ID, 'id_new_item')  
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ela digita "Estudar testes funcionais" em uma caixa de texto
        inputbox.send_keys('Estudar testes funcionais')

        # Quando ela aperta enter, a página atualiza, e mostra a lista
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Estudar testes funcionais')

        # Ainda existe uma caixa de texto convidando para adicionar outro item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')  
        inputbox.send_keys('Estudar testes de unidade')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página atualiza novamente, e agora mostra ambos os itens na sua lista
        self.check_for_row_in_list_table('1: Estudar testes funcionais')
        self.check_for_row_in_list_table('2: Estudar testes de unidade')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Maria inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Estudar testes funcionais')

        # Ela percebe que sua lista gerou uma URL única
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')

        # Agora um novo usuário, João, chega ao site.
        # Fechamos a sessão atual para garantir que nenhum dado de Maria persista
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # João visita a página inicial. A página não deve ter sinal da lista de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Estudar testes funcionais', page_text)

        # João inicia sua própria lista digitando um novo item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # João recebe sua própria URL exclusiva
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # A página de João não deve conter a lista da Maria
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Estudar testes funcionais', page_text)
        self.assertIn('Comprar leite', page_text)

if __name__ == '__main__':
    unittest.main()