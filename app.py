import streamlit as st
from fpdf import FPDF
from io import BytesIO

def fill_template(template, values):
    for i, value in enumerate(values, start=1):
        template = template.replace(f'{{value{i}}}', value)
    return template

def create_pdf(values):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_top_margin(25)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, 'Petição de juntada de substabelecimento', ln=True, align='C')

    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.multi_cell(0, 10, f'EXCELENTÍSSIMO(A) SENHOR(A) JUIZ(A) DE DIREITO DA {values[0]} VARA {values[1]}')
    pdf.multi_cell(0, 10, f'DA COMARCA DE {values[2]}')

    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f'Processo n° {values[3]}', ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f'{values[4]}, já devidamente qualificado no processo, vem, respeitosamente, solicitar a JUNTADA DE SUBSTABELECIMENTO ao procurador constituído, {values[5]}')

    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, 'DITO ISTO, requer:', ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    requests = [
        f'a) Seja juntado substabelecimento em anexo;',
        f'b) Seja anotado registrado no sistema PROJUD o nome do Advogado substabelecido para recebimento EXCLUSIVO de todas as intimações relacionadas ao processo, sob pena nulidade.',
        f'b) Seja mantido no sistema PROJUD o nome do Advogado substabelecente para permanecer recebendo {values[6]} todas as intimações relacionadas ao processo, sob pena nulidade.'
    ]

    for request in requests:
        pdf.multi_cell(0, 10, request)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f'Nesses termos, pede deferimento.\n\n{values[7]}, {values[8]}.\n{values[9]},\n{values[10]}')

    return pdf

template_text = """
EXCELENTÍSSIMO(A) SENHOR(A) JUIZ(A) DE DIREITO DA {value1} VARA {value2}
DA COMARCA DE {value3}

Processo n° {value4}

{value5}, já devidamente qualificado no processo, vem, respeitosamente, solicitar a JUNTADA DE SUBSTABELECIMENTO ao procurador constituído, {value6}

DITO ISTO, requer:
a) Seja juntado substabelecimento em anexo;
b) Seja anotado registrado no sistema PROJUD o nome do Advogado substabelecido para recebimento EXCLUSIVO de todas as intimações relacionadas ao processo, sob pena nulidade.
b) Seja mantido no sistema PROJUD o nome do Advogado substabelecente para permanecer recebendo {value7} todas as intimações relacionadas ao processo, sob pena nulidade.

Nesses termos, pede deferimento.

{value8}, {value9}.
{value10},
{value11}
"""

st.title("Document Filler")
st.subheader("Alfa Version 0.0.1")

col1, col2 = st.columns(2)

with col1:
    values = [st.text_input(f"Value {i+1}", key=f"value_{i+1}") for i in range(6)]

with col2:
    values += [st.text_input(f"Value {i+7}", key=f"value_{i+7}") for i in range(5)]

values = values[:11]


with st.form("fill_form"):
    submitted = st.form_submit_button("Generate PDF")

if submitted:
    if all(values):
        filled_text = fill_template(template_text, values)

        pdf = create_pdf(values)

        pdf_output = BytesIO()
        pdf_string = pdf.output(dest='S')
        pdf_output.write(pdf_string.encode('latin1'))
        pdf_output.seek(0)

        st.download_button(
            label="Download PDF",
            data=pdf_output.getvalue(),
            file_name="filled_document.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Please fill in all the fields before generating the PDF.")

# Add copyright notice
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: transparent;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #555;
    }
    </style>
    <div class="footer">
        Copyright © Jonatas Walker 2024
    </div>
    """, unsafe_allow_html=True
)
