import streamlit as st
import pandas as pd
import re
from io import BytesIO

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validar_email(email):
    if pd.isna(email):
        return "Vazio"
    return "Válido" if re.match(email_regex, email) else "Inválido"

st.title("📧 **Validador de E-mails**")
st.markdown("""
    Bem-vindo ao Validador de E-mails!  
    Faça o upload de qualquer arquivo CSV contendo uma coluna chamada `email` para validar os e-mails.
    O resultado será mostrado e você poderá baixar a versão validada da planilha.
""")
st.markdown("---")

arquivo = st.file_uploader("📁 **Selecione seu arquivo CSV**", type=["csv"])

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)

        # Verifica se alguma das variações de 'email' existe na planilha
        colunas_validas = ['email', 'Email', 'E-mail', 'EMAIL']
        coluna_email = None

        for col in colunas_validas:
            if col in df.columns:
                coluna_email = col
                break

        if coluna_email is None:
            st.error("❌ **Erro**: O arquivo não contém uma coluna válida de e-mails. Certifique-se de que a coluna se chame `email`, `Email`, ou `E-mail`.")
        else:
            st.info("🔍 **Validando e-mails...**")
            df['status_email'] = df[coluna_email].apply(validar_email)

            st.success("✅ **Validação concluída com sucesso!**")
            st.markdown("### **E-mails válidos:**")
            st.dataframe(df[df['status_email'] == 'Válido'][[coluna_email, 'status_email']].head(10))

            st.markdown("### **E-mails inválidos:**")
            st.dataframe(df[df['status_email'] == 'Inválido'][[coluna_email, 'status_email']].head(10))

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            st.markdown("---")
            st.download_button(
                label="📥 **Baixar arquivo validado**",
                data=csv_buffer,
                file_name="emails_validados.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"🚨 **Erro ao processar o arquivo:** {e}")

st.markdown("---")
st.markdown("Criado com ❤️ por [Miqueias Paulo da Cunha].")