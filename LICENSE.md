# Doações
<table>
    <tr>
        <td> <!-- PagSeguro -->
            <h3>
                <div align="center">PagSeguro</div>
            </h3>
            <a href="https://pag.ae/bljJm47">
            <img src="https://stc.pagseguro.uol.com.br/public/img/botoes/doacoes/120x53-doar.gif"></a>
        </td>
        <td> <!-- PayPal -->
            <h3>
                <div align="center">PayPal</div>
            </h3>
            <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=7VVS675TLJHUL&lc=BR&item_name=Eracydes%20Lima%20Carvalho%20Junior&currency_code=BRL&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted">
            <img src="https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif"></a>
        </td>
        <td> <!-- PicPay -->
            <h3>
                <div align="center">PicPay</div>
	        </h3>
            <a href="https://picpay.me/sansaoipb">
            <img src="https://lh3.googleusercontent.com/PX1pBd24_ygdLwvKMFrnUhJqGzG-YmhbYPkE8FM74qdXc-na7EqIA808F-7WAjZnvjziEESYZz2n8Ofn6WGdTrRufae_A7WbEVA5xASAUDpWNyqcVKE0GKNJrEVMBLCee5evEdrgJn8PgaI0E7qr0QDf6lTuCHI9osuziJwJ8-OTiR1JMOWLPLrw-wOW7IZ3DQCkyQECZpb_123x1K1fKNRw6cIyEWSgYRVwzX3PeljmxyH-EBOF-1wrO67-4rLP0CfbpRxJaX3pMyNlFZMLD0R6k6HvL1ax328z0qLafMwHjLPFlVEcyMkl-CFwJN9vgP37plpZ76NNruCBkj6W-MKQkvLevjcjf-Zq718N7ow8ZSlvUOCCZFJ1ieZZrLOINaMsmYGqMYpGEMME910zzAKtd-dm0IJ0TQTx_pZ0BXniK0HCvVhNHhPiYNYJGBMv_wlakLQ8XIcBdi0iIaEOFvrGSHhXEbDx6OZ9EKsvXQNoKBRwXD0Nnqxf3o-HW0U-P3pAskj3GSBa9qfvQqK-P4pxG98hYJ4st7_FA655I9n5bP-E6lIgFqvdJC8odyVfXFpHtVWfaO9_WVXowqdiXKzX9qQ9PetQNhTnJG_WgoqocmIh1FJhAYd08fonFfbmS_Hhnvi5qqxQytCqYxqWfh1elL18X8c=w120-h53-no"></a>
        </td>
    </tr>
</table>


# Graphical Notifications Zabbix - Docker
Em caso de dúvida, sugestão ou dificuldade junte-se a nós no <b>Grupo do Telegram</b> <a href="https://t.me/+bTDzmSmMPHYzOTJh" class="wikilink2" title="Ingressar no Grupo" rel="nofollow">Gráfico no Email e Telegram</a>.

O "How to" foi testado no 7.0.

# Sumário
<ul>
	<li>
		<strong>
			<a href=#requisitos>Requisitos</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#criando-chave-api-whatsapp>Chave API WhatsApp</a>
		</strong>
	</li>
    <li>
		<strong>
			<a href=#criando-chave-api-telegram>Chave API Telegram</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#edite-os-parâmetros>Parâmetros do script</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#consultando-configuração>Consultando informação</a>
		</strong>
	</li>	
    <li>
		<strong>
			<a href=#comando-para-teste>Comando de teste</a>
		</strong>
	</li>	
	<li>
		<strong>
			<a href=#configurando-envio>Configuração do front</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#arquivo-de-configuração>Detalhes sobre o arquivo de configuração</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#conclusão>Conclusão</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#contribuições>Contribuições</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#agradecimentos>Agradecimentos</a>
		</strong>
	</li>
</ul>

<br>

# Requisitos
<b>1 – </b> Ter o Docker instalado <i>(não precisa ser no Zabbix server)</i>, caso precise instalar, <a href="https://docs.docker.com/engine/install/" class="wikilink2" title="Docker install" rel="nofollow"><b>clique aqui</b></a>.<br>
<b>2 – </b> Rodar os comandos abaixo no sistema onde está o Docker</b></a>.
<h3>
Instale os pacotes:
</h3>
<blockquote> <p> Debian/Ubuntu</p> </blockquote>
<pre><code>sudo apt-get install -y wget dos2unix git sudo</code></pre>

<br>
<blockquote> <p>CentOS/Oracle Linux/Rocky Linux/Redhat+</p> </blockquote>
<pre><code>sudo dnf install -y wget dos2unix git sudo</code></pre>

<br>
<blockquote> <p>Faça o download do script de instalação</p> </blockquote>

<pre><code>cd /tmp
wget https://raw.githubusercontent.com/sansaoipb/scripts/master/notificacoes-docker.sh -O notificacoes.sh
sudo dos2unix notificacoes.sh
sudo bash notificacoes.sh
</code></pre>

<br>
<h3>
Faça o download da imagem
</h3>
<blockquote> <p>Para Telegram, Email e Teams <i>(Todos ou somente um deles)</i>: </p> </blockquote>

<pre><code>docker pull sansaoipb/notificacoes:telegram</code></pre>
<br>

<blockquote> <p>Para todas as soluções <i>(WhatsApp OpenSource, Telegram, Email e Teams)</i>: </p> </blockquote>

<pre><code>docker pull sansaoipb/notificacoes:full</code></pre>

<br>
<blockquote> <p>Subindo o container: </p> </blockquote>
<pre><code>docker run -dit -p 80:5000 -p 8080:21465 -v /etc/zabbix/scripts:/etc/zabbix/scripts \
--name sendgraph sansaoipb/notificacoes:full</code></pre>

<b>OBS: </b><br>
<b>1 – </b>Todos os exemplos abaixo considera que usará a solução completa com "WhatsApp OpenSource", caso não esteja, basta remover o parâmetro
<i>"-p 8080:21465"</i> do comando acima e alterar a tag de <i>"full"</i> para <i>"telegram"</i> em todas as referências usadas.<br>

<b>2 – </b>Os campos contidos em [PathSectionEmail], [PathSectionTelegram] e [PathSectionWhatsApp], são opcionais, logo se for usar somente telegram, não é necessário preencher a parte do email, assim como de forma inversa.<br>

# Criando Chave API WhatsApp
<h3>
Configuração do WhatsApp OpenSource
</h3>
Depois de validar que o serviço está operacional <i>(inserindo o IP no navegador)</i>, siga os próximos passos.<br>
1 - Acesse <b><u>http://IP_do_server:8080/api-docs/</u></b> e execute 2 ações nessa pagina, "/api/{session}/{secretkey}/generate-token" e "/api/{session}/start-session"<br><br>

<blockquote> <p>Gerando Token</p> </blockquote>

generate-token
<img src="https://lh3.googleusercontent.com/pw/AP1GczOjuGybwUXOqYlCCFxZwgG2YVnKpXuw_yFsqi0U--uQUAglo9TKw1sNieHOknyndy5oSUPQsQFtwXSBLJ7VKRBk6fgA_1vOY7zAEBJRjuuOciqdPZZmS_VPHzsnNfQgACvD5cpsfyiNpE2BSZ-4nFq2rw=w1879-h655-s-no-gm?authuser=0"/>

Clique em "Try it out", altere o "session", clique em "Execute" e copie o valor do atributo "token"
<img src="https://lh3.googleusercontent.com/pw/AP1GczM_dsyDWF9nmVcSQ9ff-GvqWEu68qfZFEuHp2NxjFGwcF-uGMmiOLmadMGOejErK_SAdhQhZk7DnS1dA0_hkMQggi37iRdxywMQ6fuEj77kd6_T3_Sd1xSiYQvvY9JJGIcvFJSEV_Tmtq6p-1TTm_57VA=w1868-h713-s-no-gm?authuser=0"/>

Suba até "Authorize"...
<img src="https://lh3.googleusercontent.com/pw/AP1GczOx8pNGp9nMGCuHNE4DMsQU3_htnQrO5lWV-xIXRJBbXJpRN5PXpmoADs4CnuMo4_snE2bnWAiinmZULWtILsJYslXU2RMBQGLOsUvYna17kWEdDl_WNepVa2XK0DIKEkpbcP0s7kXNcfw-O7At6r-psw=w1910-h415-s-no-gm?authuser=0"/>

Insira o token em "Value" e armazene com o botão "authorize" e depois em "Close"
<img src="https://lh3.googleusercontent.com/pw/AP1GczOuon042PdpzVwbebJ86Yv3eQp4b562a42y8-9UlADvWi1V5s9Xk_xg1QSGzmDM_3Y5iM3vG6efXwBZVbm6xg4WKqSlGZ6s1B5mLWnwCXbUy-t0zjHLBUWm4h-eii8-mrWXmW2BALJHSFE7YLbOHgjikw=w1141-h485-s-no-gm?authuser=0"/>

2 - Acesse o log da aplicação com o comando:
<pre><code>docker exec -it sendgraph pm2 logs</code></pre>

<img src="https://lh3.googleusercontent.com/pw/AP1GczN_7VoHuUnQuF9mHiZPRll3UCrF0I25xL_iaoEEySKW89Ynrrv6IqSnpvV-LLrO44t-H_IM8uK24YsLmOd3wxIo7toJpJ0i5KU0SoVi45Q-3kMHJ7SdqExrYH1BB45AKjltgk4wYBLt05tFI7O6BxLzzA=w1493-h678-s-no-gm?authuser=0"/>

Depois do log aberto, vá para "start-session", execute e posteriormente, volte ao log para ler o QR Code para conectar o WhatsApp 
<img src="https://lh3.googleusercontent.com/pw/AP1GczPWy9mAQiApoKqld0B0RGYLtTtWQ_cVuIYOhfukprQscQa8d82UuX-ew4N7q0uVw5Pb3IBOdSeyDtpILiUBHXSxXznpwonw9tLWOewfks5p4zq5yxh3zclkOZTMJR3w9vHw6RJnJzVdfpcPjOyqS3fSOg=w1856-h387-s-no-gm?authuser=0"/>


<!--
Caso o serviço não esteja OK, entre em contato no "grupo de ajuda" supracitado, para mais detalhes sobre a configuração, mas consulte o git do mantenedor e assista o video disponibilizado: <br>
<a href="https://github.com/marcilioramos/alert_wpp_zabbix" class="wikilink2" title="Acessar github" rel="nofollow">alert_wpp_zabbix</a></i>
(<a href="https://t.me/MarcilioMRTelecom" class="wikilink2" title="Conversar com ele" rel="nofollow">@MarcilioMRTelecom</a></i>)
-->

<h3>
Contratação da API para WhatsApp
</h3>

<p> Caso não queira ter a responsabilidade de manter a aplicação Open Source, existe esta opção e será necessário contratar o serviço, em conversa com o responsável consegui um desconto de 50%, 
basta informar o cupom <code><b>zabbix20S</b></code>. </p>
Para contratar acesse o site <a href="https://www.netizap.app/" title="API WhatsApp"><b>https://www.netizap.app/</b></a> <br><br>

Caso use somente o envio por WhatsApp, <b>DESCONSIDERE OS PRÓXIMOS PASSOS, e vá direto para a configuração <a href="#edite-os-parâmetros" class="wikilink2" rel="nofollow"><u>CLICANDO AQUI</u></a></b> <br>

# Criando Chave API Telegram

Para iniciarmos, <a href="https://my.telegram.org/auth?to=apps" class="wikilink2" title="API Telegram" rel="nofollow"><b>CLIQUE AQUI</b></a> e 
faça o login usando sua conta para criar a <b>chave API do Telegram</b>:

Após o login aparecerá esta tela, faça o preenchimento da forma que preferir e clique em <b>"Create application"</b>, após isso aparecerá os campos que precisamos, são eles:
o <i><b>api_id</b></i> e <i><b>api_hash</b></i>.<br><br>

<blockquote> <p>Criando 'Client App'</p> </blockquote>
<img src="https://lh3.googleusercontent.com/pw/ACtC-3dGoYhba_PHMhWr7FtUr71WylDgNox7beRdGlyJ082IicG5Xba3fIxWWk6dFeI32eTNW17CJJYz_VZIkCFLThY0XTnoHC7nYEZbSv815FOMkYSklXQpvldiOSq2C6RTiYjKybgZ8XU5yNbMXNTUfKcfVg=w984-h722-no?authuser=0"/>

# Edite os parâmetros

Para iniciarmos a configuração de envio, é preciso editar o arquivo de configuração e depois executar o script manualmente para efetivar o login, então entre no diretório <code>“que o script indicou”</code> e edite os campos abaixo contidos no arquivo <code>configScripts.properties</code>:

<b>OBS: </b><br>
<b>1 – </b>O usuário que você declarar no campo <i>“user”</i> precisa ter permissão no mínimo de leitura no ambiente.<br>

<b>2 – </b>Os campos contidos em [PathSectionEmail], [PathSectionTelegram] e [PathSectionWhatsApp], são opcionais, logo se for usar somente telegram, não é necessário preencher a parte do email, assim como de forma inversa.<br>

<b>3 – </b>Se usar gmail, é preciso alterar o acesso à conta para aplicativos, é necessário criar uma "Senha de app",<br> 
<a href="https://support.google.com/accounts/answer/185833?hl=pt-BR" class="wikilink2" title="App MAIS seguros" rel="nofollow">CRIE AQUI</a>.<br>

<blockquote>[PathSection]</blockquote>

<ul class="task-list">
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“url” = http://127.0.0.1/zabbix - URL de acesso ao FRONT com "http://" 
</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“user” = Admin
</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“pass” = zabbix
</li>
</ul>

<blockquote>[PathSectionEmail]</blockquote>
<ul class="task-list">
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“smtp_server” = smtp.gmail.com:587
</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“mail_user” = SeuEmail@gmail.com
</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“mail_pass” = SuaSenha
</li>
</ul>

<blockquote>[PathSectionTelegram]</blockquote>
<ul class="task-list">
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“api.id” = 1234567</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“api.hash” = 12asdc64vfda19df165asdvf984dbf45</li>
</ul>

<blockquote>[PathSectionWhatsApp]</blockquote>
<ul class="task-list">
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“line” = 5511950287353</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“acess.key” = XGja6Sgtz0F01rbWNDTc</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“port” = 13008</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“open.source” = no</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“open.source.url” = http://127.0.0.1/api/SendGraph</li>

<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" checked="checked" disabled="disabled">
“open.source.token” = kjhasdfgyuiwqeoihbjasdc</li>
</ul>

# Consultando Configuração

<b>OBS: </b><br>
<b>1 – </b> Caso tenha interesse em usar um dos seguintes envios: WhatsApp PAGO, Email ou Teams <i>(e <b>NÃO VAI USAR</b> o Telegram ou WhatsApp Open Source)</i>, <b>DESCONSIDERE OS PRÓXIMOS PASSOS, <a href="#comando-para-teste"><u>CLICANDO AQUI</u></a></b> <br>

<b>2 – [WHATSAPP]</b> - Você pode pesquisar pelo nome, tanto do grupo como do usuário, 
mas o envio precisa ser feito pelo ID.

<b>3 – [TELEGRAM]</b> - Caso use conta invés de bot (ou WhatsApp OpenSource), terá a vantagem de usar este módulo de consulta, 
se usar bot, este comando só servirá para finalizarmos a vinculação do remetente.<br>
Este comando, também trará a quantidade e as informações de todos os seus chats, como: Tipo, Nome, ID...<br>
Mas somente para quem estiver <b>USANDO CONTA.</b> e não <b>BOT</b>

<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --infoAll</code></pre>

<b>4 – </b> Ao executar o comando acima, será solicitado inserir o token do bot ou número de telefone da conta que será usada para envio, 
se optar por <b>usar BOT</b>, cole o token, dê ENTER e
<b>DESCONSIDERE OS PRÓXIMOS PASSOS, <a href="#comando-para-teste"><u>CLICANDO AQUI</u></a></b> <br>

<b>5 – </b> Se optar por <b>usar CONTA</b>, use a seguinte estrutura de telefone 
<code>5522988776655</code> (prefixo para o Brasil, DDD e número), 
depois que der “Enter”, receberá um código por SMS e/ou no aplicativo 
<i>(no desktop, no celular ou na versão web, basta estar logado)</i>, 
adicione o código e estará pronto.<br>

Para consultar a configuração de um usuário, grupo ou canal específico, execute o comando abaixo:

<b>Script info ID, Nome ou user.</b><br>
Exs: <br>
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "-123456789"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "Nome Sobrenome"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "usuário"</code></pre><br>

Pegue o “ID”, o “nome de cadastro” ou o "nome de registro" que aparecerá para executar o teste e posteriormente colocar no zabbix.


<b>OBS: </b><br>
<b>1 – </b> Lembrando novamente que o comando "info", <b><u>NÃO FUNCIONA COM BOT</u></b> do Telegram.<br>


<!--
<b>Script info ID, Nome ou user.</b><br>
Exs: <br>
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "-123456789"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "Nome Sobrenome"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --info "usuário"</code></pre><br>

Pegue o “ID”, o “nome de cadastro” ou o "nome de registro" que aparecerá para executar o teste e posteriormente colocar no zabbix.


<b>OBS: </b><br>
<b>1 – </b> Lembrando novamente que o comando "info", <b><u>NÃO FUNCIONA COM BOT</u></b> do Telegram.<br>


<h3><a id="user-content-features" class="anchor" href="#features" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" role="img" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>
Comando para teste
</h3>
-->

# Comando para teste

<b>OBS: </b><br>
<b>1 – </b> Para envio do WhatsApp, não é possível o envio por nome, é <b><u>SOMENTE POR "ID"</u></b>. 

<b>2 – </b>"-123456789", "Nome Sobrenome" ou "usuário" são informações fictícias para exemplificar, busque um UserID ou nome de usuário válido no seu ambiente, se for grupo ou canal use prioritáriamente o "id"; <br><br>

<b>3 – </b> A estrutura de teste para o WhatsApp será (prefixo para o Brasil, DDD e número): <code>5522988776655</code>; <br>
Para Telegram será: prioritariamente por ID (podendo usar também: 'Nome Sobrenome' ou '@usuário' se não usar bot); <br>
Para Email será: usuario@provedor.com.<br><br>

Script para realização do teste e iniciar a configuração: <br>
<b>Script, ID, Nome ou user.</b><br>
Exs: <br>
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "-123456789"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "Nome Sobrenome"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "usuário"</code></pre>
ou
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "URL_workflow"</code></pre><br>

ou para realizar 4 envios simultaneamente, basta colocar as informações separados por vírgula, por Ex:
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "-123456789, 5522988776655, usuario@provedor.com, URL_workflow"</code></pre><br>

<b>4 – </b> Para quem usa BOT, para pegar o ID (tanto do grupo/canal, como de tópico), basta copiar o link de alguma mensagem, como a estrutura abaixo.<br><br>
<b>5 – </b> Caso seja Canal ou SuperGrupo, o ID precisará ser acionado "-100" a frente do ID, conforme exemplo abaixo.<br><br>

<table>
    <td colspan="3"><div align="center"> Grupo/Canal <br>https://t.me/c/4100493856/789654</div>
        <tr>
            <td> <!-- Group/Channel -->
                <h4>
                    <div align="center">ID Grupo/Canal </div>
                </h4>
                    <div align="center">4100493856 </div>
            </td>
            <td> <!-- Message -->
                <h4>
                    <div align="center">ID Msg</div>
                </h4>
                    <div align="center">789654</div>
            </td>
        </tr>
        <td colspan="3"><div align="center"> <u>ID para envio</u><br><b>-1004100493856</b></div>
        </td>
    </td>
</table>
<br>
<b>Ex Grupo/Canal: </b><br>
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "-1004100493856"</code></pre><br>


<table>
    <td colspan="3"><div align="center">Tópico <br>https://t.me/c/4100493856/10562/789654</div>
        <tr>
            <td> <!-- Group/Channel -->
                <h4>
                    <div align="center">ID Grupo/Canal </div>
                </h4>
                    <div align="center">4100493856 </div>
            </td>
            <td> <!-- Topic -->
                <h4>
                    <div align="center">Tópico</div>
                </h4>
                <div align="center">10562</div>
            </td>
            <td> <!-- Message -->
                <h4>
                    <div align="center">ID Msg</div>
                </h4>
                    <div align="center">789654</div>
            </td>
        </tr>
        <td colspan="3"><div align="center"> <u>ID para envio</u><br><b>-1004100493856_10562</b></div>
        </td>
    </td>
</table>
<br>
<b>Ex Tópico: </b><br>
<pre><code>docker exec -it sendgraph /etc/zabbix/scripts/notificacoes-teste.py --send "-1004100493856_10562"</code></pre>

# Configurando envio

Precisamos realizar algumas configurações no Front do ZABBIX, no <i>"Tipo de Mídia"</i>, (em Alertas > Tipo de Mídia) e na <i>"Ação"</i> (em Alertas > Ações > Ações de trigger).

<h3>
Tipo de Mídia
</h3>

Importe o arquivo <bi>Notification.yaml</b>, que é o <i>"Tipo de Mídia"</i> que usaremos.

<!--
<img src="https://lh3.googleusercontent.com/pw/ACtC-3fsUm053aTiLCqXzGeHD6nhvsKSdoOlYggUCYqk1UtOIiQM6G9ZQGZjt8vs0-AxDvued87CTrHusOnTBIG7oQZPeTuHYWZNN6TTM7zGMc_AZD-L9JrLVPhO11J-FZUFBStmPlPIo1jWs1zMmokXJmFnxA=w830-h346-no?authuser=0"/><br><br>


<blockquote> Variáveis para o tipo de mídia</blockquote>
<pre><code>{ALERT.SENDTO}
{ALERT.SUBJECT}
{ALERT.MESSAGE}</code></pre>

<h3>
Configuração para envio
</h3>

Existe somente uma exigência na “<i><u>Mensagem Padrão</u></i>”, 
a primeira linha deve permanecer com as macros/variáveis abaixo ilustradas 
(<i>as macros/variáveis <b>entre as "#" </b></i>), 
podendo editar da segunda linha em diante, seja no "Modelo de mensagem" em "Tipo de mídia" ou na ação. 
<br>
-->


<h3>
Imagem da Mensagem:
</h3>

<img src="https://lh3.googleusercontent.com/pw/AM-JKLXh9DsipBWzQlk_Wqbveke7Ll21HExvenhOreIAvgzGRT87K5vdFeg_ALQdQ8vqpzMqz4r0J52NEyBN15115MK3hvOz1CcYH4Q4PAlIRCtClj1OQ6fBCFLEdTOFFdwnWueVTc5OGKriQdePNvXxfrk5Mw=w787-h393-no?authuser=0"/><br><br>

<blockquote> Modelo Mensagem (Incidente)</blockquote>
<pre><code>{TRIGGER.ID}#{EVENT.ID}#FF0000#10800#
<b>IP/DNS: </b> {HOST.CONN}
<b>Último valor: </b> {ITEM.LASTVALUE}</code></pre>
<br>
<blockquote> Modelo Mensagem (Recuperação)</blockquote>
<pre><code>{TRIGGER.ID}#{EVENT.ID}#00C800#3600#
<b>IP/DNS: </b> {HOST.CONN}
<b>Último valor: </b> {ITEM.LASTVALUE}
<b>Duração: </b> {EVENT.DURATION}</code></pre>

<b>OBS: </b><br>Os valores
<i><b>”FF0000” ou ”00C800”</b></i> são apontamentos para as informar a lista de cores que será utilizada na linha do gráfico
(alarme ou normalização), e <i><b>”10800” ou ”3600”</b></i> é o período do gráfico (3h ou 1h) em segundos.<br><br>

<h3><a id="user-content-features" class="anchor" href="#features" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" role="img" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>
Configurando o usuário
</h3>

<img src="https://lh3.googleusercontent.com/pw/ACtC-3f4gkVPqGXBGFv6xV1f_8o5YrAt0fQtOPefBTNbVvo5Zej94QpzBqyjgEsE_Q1dz0OgEBKInUu8k_jMfJVG0Oty2XqRMvJcCPawCath-M23DtCYY5UlT9xVE5Ckgk2cpbgicODDY1GyvSIQGxkdWecbbA=w844-h479-no?authuser=0"/><br><br>

<h3>
Resultado:
</h3>

<img src="https://lh3.googleusercontent.com/pw/ACtC-3dnpvrFBPMxVFEP0SiTskBrvHZVvK9bCF2BPKXbrUIrCrCumQNpc-FUfCGjONlHeRzFl8pd-ddTOU7kmOEUm1S4-CocyvPKUUqF2QyIWv3-1thy-2JvaJJqa0lLX92mTPEAmqWYIT_rcW0dpDqrC6oaVg=w542-h311-no?authuser=0"/>
<br>
<br>

# Arquivo de configuração

<br>
<i>Por sugestão de "Everaldo Santos Cabral" 
(<a href="https://t.me/everaldoscabral" class="wikilink2" title="Conversar com ele" rel="nofollow">@everaldoscabral</a>)</i>

Vamos entender um pouco as funções configuráveis do arquivo de configuração (<code>configScripts.properties</code>)

<blockquote>[PathSection]</blockquote>
<ul>
	<li>
		ack - Ativa/Desativa o ack nos eventos
	</li>
	<li>
		salutation - Ativa/Desativa todas as saudações
	</li>
	<li>
		path.logs - indica o local onde o log será salvo, o "default" é um diretório "log" no mesmo local do script, se alterar precisa garantir que o usuário zabbix tenha permissão para escrita neste local. 
	</li>
</ul>

<blockquote>[PathSectionEmail]</blockquote>
<ul>
    <li>
		salutation.email - Ativa/Desativa a saudação do email
	</li>
	<li>
		mail.from - descreve o remetente.
	</li>
</ul>

<blockquote>[PathSectionTelegram]</blockquote>
<ul>
	<li>
		salutation.telegram - Ativa/Desativa a saudação do Telegram
	</li>
	<li>
		path.graph - caminho onde a imagem para o gráfico será salvo.
	</li>
</ul>

<blockquote>[PathSectionWhatsApp]</blockquote>
<ul>
    <li>
		salutation.whatsapp - Ativa/Desativa a saudação do whatsapp
	</li>
    <li>
        open.source - Define se vc estará usando a API paga ou open source.
    </li>
    <li>
        open.source.url - Se definir o campo acima como <b>yes</b> e caso escolha outro nome de "sessão", precisará alterar na URL de SendGraph para o que escolheu: <b>http://127.0.0.1/api/nome_da_sessao_criada</b>
    </li>
    <li>
        open.source.token - Se definir o campo acima como <b>yes</b>, precisará informar o token gerado.
    </li>
</ul>

<blockquote>[PathSectionTeams]</blockquote>
<ul>
    <li>
		salutation.teams - Ativa/Desativa a saudação do whatsapp
	</li>
    <li>
        message.teams - Caso o "ack" em "PathSection" esteja habilitado, esse campo define uma mensagem que serã inserida como comentário no evento
    </li>
</ul>

# Conclusão

0 – Este script é para agilizar a análise e ficar visualmente mais agradável o recebimento dos alarmes;
<br><br>
1 - Faz uso diretamente da API do Telegram (MTProto), diferentemente da maioria (ouso até dizer todos), que usa o servidor HTTP dos BOTs, criando um ponto a mais de falha, além de ter a opção de escolher o remetente, se será um BOT ou uma conta;
<br><br>
2 - Integração API Telegram e WhatsApp: Realiza consulta para trazer informações do objeto, como Tipo (Grupo ou usuário), ID e nome (utilizado pelo script de "teste")
<br><br>
3 - Integração API ZBX (item): verificando se o item é do "tipo gráfico" (inteiro ou fracionário) para montar o gráfico se não for, ele envia somente o texto;
<br><br>
4 - Integração API ZBX (evento): Realiza ACK no evento, e insere um comentário (Pode ser desativado no arquivo de configuração);
<br><br>
5 - Existe opção de "saudação" (Bom dia, Boa tarde, Boa noite... dependendo do horário), juntamente com o nome, no caso do Telegram e "WhatsApp OpenSource", nome da pessoa, canal, ou grupo (Pode ser desativado no arquivo de configuração);
<br><br>
6 - Consegue realizar a criptografia dos campos, onde existem "informações sensíveis", como token do WhatsApp, o ID de conexão do telegram, usuário e senha do email (caso não use SMTP interno).
<br><br>
7 - Além de diversas pequenas configurações que impacta no resultado final, como: <br>
 7.1 - Flag para desconsideração do gráfico; <br>
 7.2 - Identificação e montagem do gráfico com todos os itens vinculados a trigger; <br>
 7.3 - Tratativa da data do evento, quem nunca se perguntou como alterar o padrão americano (2023.01.07) para o brasileiro (07/01/2023), a mensagem ja chega formatada; <br>
 7.4 - Tempo de gráfico personalizado... 


# Contribuições

Neste link você consegue criar de modelos para mensagens HTML, que foi indicado pelo amigo "Mario" 
(<a href="https://t.me/ZXRTI" class="wikilink2" title="Conversar com ele" rel="nofollow">@ZXRTI</a>)
<br>
<a href="https://html-online.com/editor/" class="wikilink2" title="Criador de HTML" rel="nofollow">Site para criação de modelos HTML</a>


# Agradecimentos

Gostaria de agradecer as mais de 400 pessoas que estão no "grupo dos projetos", que serve como ajuda/sugestão/contribuição
e aos que participam mais ativamente ajudando, sugerindo, pontuando, indicando melhorias e testando.

- A criação deste projeto unificado (email e telegram), foi depois de uma conversa e o de "Everaldo Santos Cabral" 
(<a href="https://t.me/everaldoscabral" class="wikilink2" title="Conversar com ele" rel="nofollow">@everaldoscabral</a>) 
dizer que a informação do arquivo de configuração era "inútil" para quem usava somente um projeto, e isso deu-me uma luz para fazer algo diferente.
<br><br>

- Hoje os projetos tem tantas melhorias e aprimoramentos, muito graças ao "Abner Klug" 
(<a href="https://t.me/abnerk" class="wikilink2" title="Conversar com ele" rel="nofollow">@abnerk</a>), 
que sempre trouxe várias ideias, como colocar opção ao ack, a saudação, dentre outras...
Todos podem colaborar para fazermos uma comunidade mais forte e projetos cada vez melhores.
<br><br>

- Ao "Gabriel R F" 
(<a href="https://t.me/GabrielRF" class="wikilink2" title="Conversar com ele" rel="nofollow">@GabrielRF</a>) 
que me apresentou ao pyrogram, me abrindo o caminho a alteração na forma de envio, 
aprimorando e dando mais possibilidades para o projeto.
<br><br>

- Ao "Marcílio MR TELECOM"
(<a href="https://t.me/MarcilioMRTelecom" class="wikilink2" title="Conversar com ele" rel="nofollow">@MarcilioMRTelecom</a>) 
que dedicou seu tempo para testar e disponibilizar o projeto da API do WhatsApp OpenSource, 
nos dando essa nova possibilidade.

Obrigado a todos os envolvidos, tanto pela disponibilidade para fazer os teste, como pela ajuda, confiança e coparticipação nos projetos.  
<br><br><br><br>

