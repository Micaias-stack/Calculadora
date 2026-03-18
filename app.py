import streamlit as st
from groq import Groq

# Configuração da página e estilo
st.set_page_config(page_title="NegociaFácil AI", page_icon="⚖️")

st.title("⚖️ NegociaFácil AI")
st.markdown("---")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔑 Acesso")
    api_key = st.text_input("Sua Groq API Key:", type="password")
    st.info("Crie sua chave gratuita em: https://console.groq.com/keys")

# --- ENTRADA DE DADOS ---
aba1, aba2, aba3 = st.tabs(["📊 Cálculo da Dívida", "💰 Sua Capacidade", "🤖 Analista de IA"])

# ABA 1: CÁLCULOS
with aba1:
    st.header("Análise do Montante")
    v_original = st.number_input("Valor original que você pegou emprestado (R$):", min_value=0.0)
    meses_atraso = st.number_input("Meses de atraso:", min_value=1, step=1)
    
    # Cálculo de referência: 1% de juros simples ao mês (base legal/justa)
    valor_referencia = v_original * (1 + (0.01 * meses_atraso))
    
    st.subheader(f"Valor Sugerido para Quitação: R$ {valor_referencia:.2f}")
    st.caption("Baseado em juros simples de 1% ao mês.")

# ABA 2: ORÇAMENTO
with aba2:
    st.header("Sua Realidade Financeira")
    renda = st.number_input("Quanto você ganha por mês (Líquido):", min_value=0.0)
    gastos = st.number_input("Quanto você gasta com o essencial (Aluguel, Luz, Comida):", min_value=0.0)
    
    sobra = renda - gastos
    if sobra > 0:
        p_segura = sobra * 0.25  # Regra de 25% da sobra para não sufocar o usuário
        st.success(f"Sua sobra livre é de R$ {sobra:.2f}")
        st.write(f"### 🛡️ Sua parcela máxima: **R$ {p_segura:.2f}**")
    else:
        p_segura = 0
        st.error("Atenção: Seu orçamento está no limite. Não recomendamos aceitar parcelamentos agora.")

# ABA 3: INTELIGÊNCIA ARTIFICIAL
with aba3:
    st.header("Analisar Proposta com IA")
    proposta_texto = st.text_area("Copie e cole aqui o texto da proposta que o banco te enviou:", height=150)
    
    if st.button("Analisar Agora"):
        if not api_key:
            st.error("Por favor, insira sua Chave API do Groq na barra lateral.")
        elif not proposta_texto:
            st.warning("Cole o texto da proposta para continuar.")
        else:
            try:
                # Inicializa o cliente Groq atualizado
                client = Groq(api_key=api_key)
                
                # Monta o contexto para a IA
                prompt_ia = f"""
                Você é um consultor financeiro especialista em dívidas.
                O usuário tem uma dívida original de R$ {v_original:.2f} atrasada há {meses_atraso} meses.
                O valor justo calculado foi R$ {valor_referencia:.2f}.
                O usuário pode pagar NO MÁXIMO parcelas de R$ {p_segura:.2f}.
                
                Analise esta proposta do banco: "{proposta_texto}"
                
                Dê um veredito: 
                1. A proposta é justa ou abusiva? 
                2. Cabe no orçamento dele (R$ {p_segura:.2f}/mês)? 
                3. Escreva uma contraproposta curta para ele enviar ao banco.
                """
                
                # Chamada para o modelo mais rápido e atualizado (Llama 3 70B)
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_ia}],
                    model="llama3-70b-8192",
                )
                
                st.subheader("💡 Análise da IA:")
                st.info(chat_completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Erro na conexão com a IA: {e}")

st.markdown("---")
st.caption("Desenvolvido para apoio à educação financeira.")
