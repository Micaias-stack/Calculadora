import streamlit as st
from groq import Groq

st.set_page_config(page_title="NegociaFácil AI", page_icon="⚖️", layout="wide")

api_key = "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"

# --- SIDEBAR: ORÇAMENTO ---
with st.sidebar:
    st.header("📋 MEU ORÇAMENTO")
    salario = st.number_input("Salário/Renda (R$):", min_value=0.0, value=2000.0)
    gastos = st.number_input("Gastos Fixos (Aluguel/Luz/etc):", min_value=0.0, value=1500.0)
    sobra = salario - gastos
    st.metric("Sobra Mensal", f"R$ {sobra:.2f}")

# --- CORPO PRINCIPAL ---
st.title("⚖️ NegociaFácil AI")

tab1, tab2 = st.tabs(["💰 Sugestão de Acordo", "🤖 Gerar Texto para o Banco"])

with tab1:
    st.header("Qual o valor justo para quitar?")
    divida_total = st.number_input("Valor total da dívida hoje (R$):", min_value=0.0, value=1446.18)
    
    st.subheader("Sugestões de Contraproposta (À Vista)")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Proposta 1 (50% desc.)", f"R$ {divida_total * 0.5:.2f}")
    c2.metric("Proposta 2 (35% desc.)", f"R$ {divida_total * 0.65:.2f}")
    c3.metric("Proposta 3 (25% desc.)", f"R$ {divida_total * 0.75:.2f}")
    
    st.info("💡 **Dica:** Comece oferecendo a 'Proposta 1'. Se o banco negar, suba para a 2. Nunca aceite o valor cheio se você teve problemas de saúde comprovados.")

with tab2:
    st.header("🤖 Criar Mensagem de Negociação")
    detalhes = st.text_area("Explique brevemente o motivo do atraso:", 
                            "Sofri um acidente há um ano, a dívida acumulou, mas já paguei parte dela. Quero quitar o saldo de 1.446,18 à vista.")
    
    if st.button("Gerar Texto"):
        try:
            client = Groq(api_key=api_key)
            prompt = f"O usuário deve R$ {divida_total}. Ele sofreu um acidente e já pagou parte. Gere um texto para ele enviar no chat do banco pedindo desconto para quitar à vista agora."
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            st.success("Copie e envie para o banco:")
            st.write(chat.choices[0].message.content)
        except Exception as e:
            st.error(f"Erro na IA: {e}")

st.markdown("---")
st.caption("Desenvolvido para ajudar na recuperação financeira.")
