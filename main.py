#  -----------------------------------------------------------------------
#   .* APLICATIVO COM KIVY - PYTHON - FIREBASE *.
# 
#    main.py - Arquivo do programa principal
# 
#    Copyright 2022 Ludmila Dias
# 
#   ----------------------------------------------------------------------

# IMPORTAÇÃO DE BIBLIOTECAS E MÓDULOS
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
import database
import json
import requests


#   DECLARAÇÃO INICIAL DE VARIAVEIS
GUI=Builder.load_file("tela.kv")
cpf_usuario=""
dados_usuario=[]
email_senha=""


class Manager(ScreenManager):
    pass

#   TELA DE LOGIN
class LoginScreen(MDScreen):

#   FUNÇÃO QUE SE REALIZA LOGO NA ABERTURA DA TELA
    def on_pre_enter(self, *args):
        try:
            self.ids.text_email.text = ""
            self.ids.text_password.text = ""
            self.ids.label_login.text = ""
        except:
            pass
#   FUNÇÃO PARA REALIZAR O LOGIN        
    def try_sign_in(self):
        global cpf_usuario
        if self.ids.text_email.text != "" and self.ids.text_password.text != "":
            if database.verificar_login(self.ids.text_email.text,self.ids.text_password.text):
                cpf_usuario=self.ids.text_email.text
                MDApp.get_running_app().root.current = "home_page"
            else:
                self.ids.label_login.text = "Senha ou CPF incorreto."

#   TELA DE HOMEPAGE DO APLICATIVO
class HomePage(MDScreen):
    def on_pre_enter(self, *args):
        global dados_usuario
        dados_usuario=database.acessar_dados_usuario(cpf_usuario)
        self.ids.label_nome.text=dados_usuario[2]
    
    def logout(self):
        self.dados_usuario=[]
        self.cpf_usuario=""
        MDApp.get_running_app().root.current = "login"

    def callback(self):
        MDApp.get_running_app().root.current = "login"

#   TELA 1 PARA REDEFINIR SENHA (NÃO INCLUI ENVIO DE E-MAIL)
class ResetPassword(MDScreen):
    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

    def on_pre_enter(self, *args):
        self.ids.email_confirm.text = ""
        self.ids.text_redefined.theme_text_color = "Primary"

    def button_password(self):
        global email_senha
        email_senha = self.ids.email_confirm.text
        MDApp.get_running_app().root.current = "new_password"

#   TELA 2 PARA REDEFINIR SENHA
class NewPassword(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.label_novasenha.text = ""
        self.ids.label_confirma.text = ""
        self.ids.label_sucesso.text = ""
        self.ids.label_newps.text = "Insira uma nova senha"
        self.ids.label_newps.theme_text_color = "Primary"
        

    def alterar_senha(self):
        global email_senha
        if self.ids.label_novasenha.text != "" and self.ids.label_confirma.text != "" :
            if self.ids.label_novasenha.text == self.ids.label_confirma.text :
                
                if (database.redefinir_senha(email_senha, self.ids.label_novasenha.text)):
                    self.ids.label_sucesso.text = "Senha Redefinida com Sucesso"
                    Clock.schedule_once(self.callback, 5)
                else:
                    self.ids.label_sucesso.text = "Erro, tente novamente."
            else:
                self.ids.label_sucesso.text = "As senhas não coincidem."

    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

#   TELA DE CADASTRO
class Register(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.name_register.text = ""
        self.ids.email_register.text = ""
        self.ids.password_register.text = ""
        self.ids.password_register_confirm.text = ""
        self.ids.cpf_register.text = ""
        self.ids.label_sucess.text = ""
        self.ids.label_register.text = "Insira seus dados"
        self.ids.label_register.theme_text_color = "Primary"

    def cadastrar(self):
        if self.ids.email_register.text != "" and self.ids.password_register.text != "" and self.ids.password_register_confirm.text != "" and self.ids.password_register_confirm.text != "" and self.ids.name_register.text != "" :
            if database.verifica_cpf_cadastro(self.ids.cpf_register.text):
                if database.cpf_validate(self.ids.cpf_register.text):
                    if database.verifica_email_cadastro(self.ids.email_register.text):
                        if self.ids.password_register.text == self.ids.password_register_confirm.text:
                            if database.cadastro_usuario(self.ids.name_register.text, self.ids.email_register.text,self.ids.cpf_register.text,self.ids.password_register.text):
                                self.ids.label_sucess.text = "Cadastro realizado com sucesso!"
                                Clock.schedule_once(self.callback, 5)
                            else:
                                self.ids.label_sucess.text = "Erro tente novamente."
                        else:
                            self.ids.label_sucess.text = "As senhas não coincidem."
                    else:
                        self.ids.label_sucess.text = "E-mail já cadastrado."
                else:
                    self.ids.label_sucess.text = "CPF inválido."     
            else:
                self.ids.label_sucess.text = "CPF já cadastrado."

    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

#   TELA DE MENU DE AGENDAMENTOS
class Agendar(MDScreen):
    def on_pre_enter(self, *args):
        pass
    def callback(self):
        MDApp.get_running_app().root.current = "home_page"

#   TELA DE AGENDAMENTO DE CONSULTAS
class AgendamentoConsulta(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.data_agenda.text = ""
        self.ids.especialidade_agenda.text = ""
        self.ids.paciente_agenda.text = ""
        self.ids.label_agenda.text=""
    def agendar_consulta(self):
        if self.ids.paciente_agenda.text!="" and self.ids.especialidade_agenda.text!="" and self.ids.data_agenda.text!="":
            if database.cpf_validate(self.ids.paciente_agenda.text):
                if database.verifica_cpf_agendamento(self.ids.paciente_agenda.text):
                    if database.agendar_consulta(self.ids.paciente_agenda.text, self.ids.especialidade_agenda.text, self.ids.data_agenda.text):
                        self.ids.label_agenda.text="Agendamento feito com sucesso!"
                        Clock.schedule_once(self.callback, 5)
                    else:
                        self.ids.label_agenda.text="Erro, tente novamente!"
                else:
                    self.ids.label_agenda.text="Paciente não cadastrado."
            else:
                self.ids.label_agenda.text="CPF inválido."
    def callback(self, *args):
        MDApp.get_running_app().root.current = "agendar"

#   TELA DE AGENDAMENTO DE RETIRADA
class AgendamentoRetirada(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.data_retirada.text = ""
        self.ids.medicamento_retirada.text = ""
        self.ids.paciente_retirada.text = ""
        self.ids.label_retirada.text=""
    def agendar_retirada(self):
        if self.ids.paciente_retirada.text!="" and self.ids.medicamento_retirada.text!="" and self.ids.data_retirada.text!="":
            if database.cpf_validate(self.ids.paciente_retirada.text):
                if database.verifica_cpf_agendamento(self.ids.paciente_retirada.text):
                    if database.verifica_medicamento(self.ids.medicamento_retirada.text):
                        if database.verifica_estoque(self.ids.medicamento_retirada.text):
                            if database.agendar_retirada(self.ids.paciente_retirada.text, self.ids.medicamento_retirada.text, self.ids.data_retirada.text):
                                self.ids.label_retirada.text="Agendamento feito com sucesso!"
                                Clock.schedule_once(self.callback, 5)
                            else:
                                self.ids.label_retirada.text="Erro, tente novamente!"
                        else:
                            data=database.verifica_remessa(self.ids.medicamento_retirada.text)
                            self.ids.label_retirada.text=f"Medicamento sem estoque. Prox. Remessa em: {data}"
                    else:
                        self.ids.label_retirada.text="Medicamento não listado"
                else:
                    self.ids.label_retirada.text="Paciente não cadastrado."
            else:
                self.ids.label_retirada.text="CPF inválido."
    def callback(self, *args):
        MDApp.get_running_app().root.current = "agendar"

#   TELA COM TABELA DE PACIENTES
class TabelaPacientes(MDScreen):
    def on_pre_enter(self, *args):
        table = MDDataTable(
		    pos_hint = {'center_x': 0.5, 'center_y': 0.5},
			size_hint =(0.9, 0.6),
			column_data = [
				("CPF", dp(40)),
				("Nome", dp(30)),
				("Telefone", dp(30)),
			],
			row_data = database.dadosPacientes()
        )

		#return Builder.load_file('table.kv')
		# Add table widget to screen
        self.add_widget(table)
    
    
    def callback(self):
        MDApp.get_running_app().root.current = "home_page"
    
#   TELA COM TABELA E CONTROLE DE ESTOQUE DE MEDICAMENTOS
class TabelaMedicamentos(MDScreen):
    table=()
    def on_pre_enter(self, *args):
        self.ids.label_controle.text=""
        self.ids.label_estoque.text=""
        self.ids.label_idmed.text=""
        self.table = MDDataTable(
		    pos_hint = {'center_x': 0.5, 'center_y': 0.63},
			size_hint =(0.9, 0.45),
			column_data = [
				("ID", dp(30)),
				("Nome", dp(30)),
				("Quant.", dp(30)),
                ("Prox. Remessa", dp(30)),
			],
			row_data = database.dadosMedicamentos()
        )


		#return Builder.load_file('table.kv')
		# Add table widget to screen
        self.add_widget(self.table)
    
    def saida_meds(self):

        if self.ids.label_controle.text != "" and self.ids.label_idmed.text != "":
            if database.verifica_meddado(self.ids.label_idmed.text):
                if database.atualizarEstoque(self.ids.label_idmed.text, self.ids.label_controle.text,"s"):
                    self.ids.label_estoque.text = "Alteração feita com sucesso!"
                    Clock.schedule_once(self.on_pre_enter, 2)
                else:
                    self.ids.label_estoque.text = "Erro, tente novamente."
            else:
                    self.ids.label_estoque.text = "ID incorreto."
    
    def entrada_meds(self):
            if self.ids.label_controle.text != "" and self.ids.label_idmed.text != "":
                if database.verifica_meddado(self.ids.label_idmed.text):
                    if database.atualizarEstoque(self.ids.label_idmed.text, self.ids.label_controle.text,"e"):
                        self.ids.label_estoque.text = "Alteração feita com sucesso!"
                        Clock.schedule_once(self.on_pre_enter, 4)
                    else:
                        self.ids.label_estoque.text = "Erro, tente novamente."
                else:
                    self.ids.label_estoque.text = "ID incorreto."
        
    def callback(self):
        MDApp.get_running_app().root.current = "home_page"

#   TELA DO PERFIL DO USUÁRIO + INFORMAÇÕES DE AGENDAMENTOS
class Perfil(MDScreen):
    table=()
    def on_pre_enter(self, *args):
        self.ids.nome_usu.text=dados_usuario[2]
        self.ids.email_usu.text=dados_usuario[3]
        self.table = MDDataTable(
		    pos_hint = {'center_x': 0.5, 'center_y': .3},
			size_hint =(0.9, 0.32),
			column_data = [
				("ID", dp(20)),
				("Paciente", dp(30)),
				("Data", dp(30)),
                ("Tipo", dp(30)),
			],
			row_data = database.dadosAgendamentos()
        )

        self.add_widget(self.table)

    def callback(self):
        MDApp.get_running_app().root.current = "home_page"

#   TELA PARA EDITAR DADOS DO USUÁRIO
class EditarDados(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.nome_perfil.text=dados_usuario[2]
        self.ids.cpf_perfil.text=dados_usuario[1]
        self.ids.email_perfil.text=dados_usuario[3]
        self.ids.senha_perfil.text=dados_usuario[4]
        self.ids.alterar_result.text=""
    
    def alterar_dados(self):
        global dados_usuario
        if database.alterar_dados(dados_usuario[0],self.ids.nome_perfil.text,self.ids.email_perfil.text,self.ids.cpf_perfil.text,self.ids.senha_perfil.text):
            self.ids.alterar_result.text="Alteração feita com sucesso!"
            id=dados_usuario[0]
            dados_usuario=[id,self.ids.cpf_perfil.text, self.ids.nome_perfil.text, self.ids.email_perfil.text,self.ids.senha_perfil.text]
        else:
            self.ids.alterar_result.text="Erro, tente novamente."
    def callback(self):
        MDApp.get_running_app().root.current = "perfil"

class MyApp(MDApp):
    Window.size = (400, 600)


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Manager()#Builder.load_file("myapp.kv")


if __name__ == "__main__":

    MyApp().run()