import streamlit as st

# Configuração da página
st.set_page_config(page_title="NegociaFácil", page_icon="🤝")

st.title("🤝 NegociaFácil")
st.markdown("---")

# --- ABA DE NAVEGAÇÃO ---
menu = ["Calculadora de Dívida", "Capacidade de Pagamento", "Gerar Contraproposta"]
escolha = st.sidebar.selectbox("Selecione uma ferramenta:", menu)

if escolha == "Calculadora de Dívida":
    st.header("📉 Análise da Dívida Atual")
    
    col1, col2 = st.columns(2)
    with col1:
        valor_original = st.number_input("Valor original da dívida (R$):", min_value=0.0, step=100.0)
    with col2:
        meses_atraso = st.number_input("Meses em atraso:", min_value=1, step=1)
    
    proposta_banco = st.number_input("Qual o valor total da proposta do banco? (R$):", min_value=0.0)

    if valor_original > 0:
        # Cálculo sugerido: Inflação estimada + Juros simples de 1% ao mês (parâmetro de negociação)
        valor_justo = valor_original * (1 + (0.01 * meses_atraso))
        
        st.subheader("💡 Nossa Sugestão")
        st.write(f"Um valor justo para quitação seria em torno de: **R$ {valor_justo:.2f}**")
        
        diferenca = proposta_banco - valor_justo
        if proposta_banco > 0:
            if diferenca > 0:
                st.warning(f"Atenção: A proposta do banco está R$ {diferenca:.2f} acima do cálculo sugerido.")
            else:
                st.success("A proposta do banco parece estar dentro de um limite justo!")

elif escolha == "Capacidade de Pagamento":
    st.header("💰 Quanto você pode pagar?")
    st.info("Nunca aceite um acordo que comprometa mais de 20% da sua renda livre.")
    
    renda = st.number_input("Sua renda mensal líquida (R$):", min_value=0.0, step=100.0)
    gastos_fixos = st.number_input("Soma de gastos fixos (Aluguel, Luz, Comida) (R$):", min_value=0.0, step=100.0)
    
    sobra = renda - gastos_fixos
    
    if sobra > 0:
        parcela_ideal = sobra * 0.20
        st.success(f"Sua sobra mensal é de R$ {sobra:.2f}")
        st.write(f"### 🛡️ Parcela Segura: **R$ {parcela_ideal:.2f}**")
        st.caption("Baseado na regra de 20% da sua sobra financeira.")
    else:
        st.error("Seus gastos estão maiores que sua renda. Priorize o essencial antes de negociar parcelas.")

elif escolha == "Gerar Contraproposta":
    st.header("📝 Modelo de Mensagem")
    st.write("Copie o texto abaixo para enviar ao gerente ou no chat:")
    
    texto_modelo = """
    Olá, gostaria de formalizar uma contraproposta para a dívida X. 
    Analisei minha capacidade de pagamento e, para que o acordo seja cumprido sem atrasos, 
    consigo oferecer uma entrada de R$ [INSIRA VALOR] e parcelas de R$ [INSIRA VALOR].
    Aguardo retorno sobre a viabilidade desta proposta justa para ambas as partes.
    """
    st.text_area("Mensagem para copiar:", texto_modelo, height=200)

st.markdown("---")
st.caption("Desenvolvido para ajudar na educação financeira e negociações justas.")
