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

O "How to" foi testado no ZABBIX 3.0 ao 7.0.

# Sumário
<ul>
	<li>
		<strong>
			<a href=#requisitos>Requisitos</a>
		</strong>
	</li>
    <li>
		<strong>
			<a href=#comando-para-teste>Comando de teste</a>
		</strong>
	</li>	
</ul>

<br>

# Requisitos
<b>1 – </b> Ter o Docker instalado no Zabbix server, caso precise, <a href="https://docs.docker.com/engine/install/" class="wikilink2" title="API Telegram" rel="nofollow"><b>clique aqui</b></a>.
<h3>
Instale os pacotes:
</h3>
<blockquote> <p> Debian/Ubuntu</p> </blockquote>
<pre><code>sudo apt-get install -y wget dos2unix git sudo curl bc</code></pre>

<br>
<blockquote> <p>CentOS/Oracle Linux/Rocky Linux/Redhat+</p> </blockquote>
<pre><code>sudo dnf install -y wget dos2unix git sudo curl bc gcc libffi-devel python3-devel openssl-devel libevent-devel</code></pre>

<br>
<blockquote> <p>Faça o download do script de instalação</p> </blockquote>

<pre><code>cd /tmp
wget https://raw.githubusercontent.com/sansaoipb/scripts/master/notificacoes-docker.sh -O notificacoes.sh
sudo dos2unix notificacoes.sh
sudo bash notificacoes.sh

</code></pre>

<br>
<blockquote> <p>Faça o download da imagem</p> </blockquote>

<pre><code>docker pull sansaoipb/notificacoes:telegram</code></pre>

# Comando para teste

<b>OBS:</b><br>
<b>0 – </b> Para envio do WhatsApp, não é possivel o envio por nome, é <b><u>SOMENTE POR "ID"</u></b>. 

<b>1 – </b>"-123456789", "Nome Sobrenome" ou "usuário" são informações fictícias para exemplificar, busque um UserID ou nome de usuário válido no seu ambiente, se for grupo ou canal use prioritáriamente o "id";<br><br>

<b>2 – </b> É recomendado aumentar o tempo de timeout da aplicação, então no arquivo de configuração do server.<br>
(se não mudou o local padrão, estará aqui <code>/etc/zabbix/zabbix_server.conf</code> ou aqui <code>/usr/local/etc/zabbix_server.conf</code>)
vá até o paramemtro <code>\# Timeout=3</code> descomente e aumente para 30, ficando assim: 
<code>Timeout=30</code><br>
dessa forma fica garantido a entrega.<br><br>
<b>3 – </b> A estrutura de teste para o WhatsApp será (prefixo para o Brasil, DDD e número): <code>5522988776655</code>;<br>
Para Telegram será: prioritariamente por ID (podendo usar também: 'Nome Sobrenome' ou '@usuário' se não estiver usando bot);<br>
Para Email será: usuario@provedor.com.<br><br>

Script para realização do teste e iniciar a configuração:<br>
<b>Script, ID, Nome ou user.</b><br>
Exs:<br>
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "-123456789"</code></pre>
ou
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "Nome Sobrenome"</code></pre>
ou
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "usuário"</code></pre><br>
ou para realizar 3 envios simultaneomente, basta colocar as informações separados por vígula, por Ex:
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "-123456789, 5522988776655, usuario@provedor.com"</code></pre><br>

<b>4 – </b> Para quem usa BOT, para pegar o ID (tanto do grupo/canal, como de tópico), basta copiar o link de alguma mensagem, como a estrutura abaixo.<br><br>
<b>5 – </b> Caso seja Canal ou SuperGrupo, o ID precisará ser acionado "-100" a frente do ID, confome exemplo abaixo.<br><br>

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
<b>Ex Grupo/Canal:</b><br>
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "-1004100493856"</code></pre><br>


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
<b>Ex Tópico:</b><br>
<pre><code>docker run -v /etc/zabbix/scripts:/opt/scripts/ --rm -it sansaoipb/notificacoes:telegram /opt/scripts/notificacoes-teste.py --send "-1004100493856_10562"</code></pre>
