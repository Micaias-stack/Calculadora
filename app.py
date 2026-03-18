import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="NegociaFácil AI", page_icon="⚖️", layout="wide")

# SUA CHAVE API CONFIGURADA
api_key = "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"

# --- BARRA LATERAL: ORÇAMENTO MENSAL ---
with st.sidebar:
    st.header("📋 ORÇAMENTO MENSAL")
    st.write("Preencha para calcular sua sobra:")
    
    # Entradas
    st.subheader("Entradas")
    salario = st.number_input("Salário Líquido (R$):", min_value=0.0, step=50.0)
    outras_rendas = st.number_input("Outras Rendas (R$):", min_value=0.0, step=50.0)
    total_entradas = salario + outras_rendas
    
    # Saídas
    st.subheader("Saídas (Gastos)")
    aluguel = st.number_input("Aluguel/Moradia (R$):", min_value=0.0, step=50.0)
    cartao = st.number_input("Fatura Cartão (R$):", min_value=0.0, step=50.0)
    contas_fixas = st.number_input("Luz, Água e Net (R$):", min_value=0.0, step=10.0)
    lazer = st.number_input("Lazer/Outros (R$):", min_value=0.0, step=10.0)
    total_saidas = aluguel + cartao + contas_fixas + lazer
    
    st.markdown("---")
    
    # Resultado no Sidebar
    sobra_final = total_entradas - total_saidas
    st.metric("Sobra Livre", f"R$ {sobra_final:.2f}")
    
    if sobra_final <= 0:
        st.error("Atenção: Você está no vermelho!")
    else:
        p_segura = sobra_final * 0.25
        st.success(f"Parcela Segura: R$ {p_segura:.2f}")

# --- CORPO PRINCIPAL DO APP ---
st.title("⚖️ NegociaFácil AI")
st.write("Use os dados do seu orçamento ao lado para analisar suas dívidas abaixo.")

aba1, aba2 = st.tabs(["📊 Cálculo da Dívida", "🤖 Analista de IA"])

with aba1:
    st.header("Análise do Montante")
    col_a, col_b = st.columns(2)
    
    with col_a:
        v_original = st.number_input("Valor original da dívida (R$):", min_value=0.0)
    with col_b:
        meses_atraso = st.number_input("Meses de atraso:", min_value=1, step=1)
    
    valor_referencia = v_original * (1 + (0.01 * meses_atraso))
    
    st.markdown("### Resumo da Análise")
    c1, c2 = st.columns(2)
    c1.metric("Valor Sugerido (1% am)", f"R$ {valor_referencia:.2f}")
    
    if sobra_final > 0:
        c2.metric("Sua Capacidade Mensal", f"R$ {p_segura:.2f}")

with aba2:
    st.header("Analisar Proposta com IA")
    proposta_texto = st.text_area("Cole aqui a proposta do banco ou credor:", height=200)
    
    if st.button("Analisar com Inteligência Artificial"):
        if not proposta_texto:
            st.warning("Por favor, cole o texto para análise.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                # Contexto rico para a IA
                prompt_ia = f"""
                Você é um consultor de dívidas. 
                Dados do cliente:
                - Dívida Original: R$ {v_original:.2f}
                - Tempo: {meses_atraso} meses
                - Sobra Mensal Real: R$ {sobra_final:.2f}
                - Parcela Máxima que ele aguenta: R$ {p_segura if sobra_final > 0 else 0:.2f}
                
                Proposta recebida: "{proposta_texto}"
                
                Diga se a proposta é abusiva, se cabe no orçamento de R$ {sobra_final:.2f} 
                e sugira uma contraproposta baseada no valor de R$ {valor_referencia:.2f}.
                """
                
                with st.spinner("A IA está analisando..."):
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt_ia}],
                        model="llama3-70b-8192",
                    )
                    st.subheader("💡 Parecer do Especialista AI")
                    st.info(chat_completion.choices[0].message.content)
                    
            except Exception as e:
                st.error(f"Erro na conexão: {e}")

st.markdown("---")
st.caption("Foco em transparência financeira e negociações justas.")
