import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="NegociaFácil AI", page_icon="⚖️")

# --- SUA CHAVE API CONFIGURADA ---
# Inseri a chave que você enviou diretamente na variável abaixo
api_key = "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"

st.title("⚖️ NegociaFácil AI")
st.markdown("---")

# --- NAVEGAÇÃO ---
aba1, aba2, aba3 = st.tabs(["📊 Cálculo da Dívida", "💰 Sua Capacidade", "🤖 Analista de IA"])

with aba1:
    st.header("Análise do Montante")
    v_original = st.number_input("Valor original da dívida (R$):", min_value=0.0)
    meses_atraso = st.number_input("Meses de atraso:", min_value=1, step=1)
    
    # Cálculo de referência (Juros simples de 1% ao mês)
    valor_referencia = v_original * (1 + (0.01 * meses_atraso))
    st.subheader(f"Valor Sugerido para Quitação: R$ {valor_referencia:.2f}")
    st.caption("Sugestão baseada em juros de 1% am.")

with aba2:
    st.header("Sua Realidade Financeira")
    renda = st.number_input("Sua renda mensal líquida:", min_value=0.0)
    gastos = st.number_input("Seus gastos fixos totais:", min_value=0.0)
    
    sobra = renda - gastos
    p_segura = sobra * 0.25 if sobra > 0 else 0
    
    if sobra > 0:
        st.success(f"Sua sobra livre é R$ {sobra:.2f}")
        st.write(f"### 🛡️ Sua parcela máxima: **R$ {p_segura:.2f}**")
    else:
        st.error("Orçamento no limite. Evite novos parcelamentos.")

with aba3:
    st.header("Analisar Proposta com IA")
    st.write("A IA usará os dados das abas anteriores para analisar o texto abaixo.")
    proposta_texto = st.text_area("Cole aqui o texto ou proposta do banco:", height=150)
    
    if st.button("Analisar Proposta"):
        if not proposta_texto:
            st.warning("Por favor, cole o texto da proposta para a IA analisar.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                prompt_ia = f"""
                Você é um consultor especialista em dívidas. 
                Dívida original: R$ {v_original:.2f} ({meses_atraso} meses atrás).
                Nosso valor justo calculado: R$ {valor_referencia:.2f}.
                Capacidade de pagamento mensal do usuário: R$ {p_segura:.2f}.
                
                Analise esta proposta: "{proposta_texto}"
                
                Responda de forma clara:
                1. A proposta é abusiva ou aceitável?
                2. O valor da parcela cabe no limite de R$ {p_segura:.2f}?
                3. Sugira uma contraproposta curta.
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_ia}],
                    model="llama3-70b-8192",
                )
                
                st.subheader("💡 Veredito da IA:")
                st.info(chat_completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Ocorreu um erro na análise: {e}")

st.markdown("---")
st.caption("App desenvolvido para auxílio em negociações financeiras.")
