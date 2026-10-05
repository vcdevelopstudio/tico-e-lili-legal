const SUPPORTED_LANGUAGES = ["pt-BR", "en-US", "es-ES"];
const FALLBACK_LANGUAGE = "pt-BR";

const homeContent = {
  "pt-BR": {
    title: "Tico e Lili: Cristal Arco-Íris",
    intro: "Encontre os documentos legais do jogo.",
    privacyTitle: "Política de Privacidade",
    privacyDetail: "Como o jogo trata dados e preferências.",
    termsTitle: "Termos de Uso",
    termsDetail: "Regras de uso e compra do jogo completo.",
    support: "Contato de suporte:",
    pageTitle: "Documentos legais | Tico e Lili: Cristal Arco-Íris"
  },
  "en-US": {
    title: "Tico e Lili: Cristal Arco-Íris",
    intro: "Find the game's legal documents.",
    privacyTitle: "Privacy Policy",
    privacyDetail: "How the game handles data and preferences.",
    termsTitle: "Terms of Use",
    termsDetail: "Rules for using and purchasing the full game.",
    support: "Support contact:",
    pageTitle: "Legal documents | Tico e Lili: Cristal Arco-Íris"
  },
  "es-ES": {
    title: "Tico e Lili: Cristal Arco-Íris",
    intro: "Encuentra los documentos legales del juego.",
    privacyTitle: "Política de Privacidad",
    privacyDetail: "Cómo el juego trata los datos y las preferencias.",
    termsTitle: "Términos de Uso",
    termsDetail: "Reglas de uso y compra del juego completo.",
    support: "Contacto de soporte:",
    pageTitle: "Documentos legales | Tico e Lili: Cristal Arco-Íris"
  }
};

const languageButtons = [...document.querySelectorAll("[data-language]")];
const legalRoot = document.querySelector("#legal-document");
let loadedDocument = null;

function normalizeLanguage(language) {
  return SUPPORTED_LANGUAGES.includes(language) ? language : FALLBACK_LANGUAGE;
}

function setActiveLanguage(language) {
  const resolvedLanguage = normalizeLanguage(language);
  document.documentElement.lang = resolvedLanguage;
  languageButtons.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.language === resolvedLanguage));
  });
  return resolvedLanguage;
}

function setText(id, value) {
  const element = document.querySelector(`#${id}`);
  if (element) element.textContent = value;
}

function renderHome(language) {
  const content = homeContent[language];
  setText("site-title", content.title);
  setText("home-intro", content.intro);
  setText("privacy-link-title", content.privacyTitle);
  setText("privacy-link-detail", content.privacyDetail);
  setText("terms-link-title", content.termsTitle);
  setText("terms-link-detail", content.termsDetail);
  setText("support-note", content.support);
  document.title = content.pageTitle;
}

function appendTextElement(parent, tagName, text, className = "") {
  const element = document.createElement(tagName);
  element.textContent = text;
  if (className) element.className = className;
  parent.appendChild(element);
}

function renderLegalDocument(language) {
  const content = loadedDocument?.[language];
  const documentContent = document.querySelector("#document-content");
  if (!content || !documentContent) return;

  setText("back-link", content.back);
  setText("related-document", legalRoot.dataset.document === "privacy_policy"
    ? homeContent[language].termsTitle : homeContent[language].privacyTitle);
  documentContent.replaceChildren();
  appendTextElement(documentContent, "h1", content.title);
  appendTextElement(documentContent, "p", content.updated, "updated");
  if (content.publisher) appendTextElement(documentContent, "p", content.publisher, "updated");
  content.sections.forEach((section) => {
    appendTextElement(documentContent, "h2", section.title);
    appendTextElement(documentContent, "p", section.body);
    (section.links || []).forEach((link) => {
      if (!link.url.startsWith("https://")) return;
      const paragraph = document.createElement("p");
      paragraph.className = "policy-link";
      const anchor = document.createElement("a");
      anchor.href = link.url;
      anchor.textContent = link.label;
      paragraph.appendChild(anchor);
      documentContent.appendChild(paragraph);
    });
  });
  document.title = `${content.title} | Tico e Lili: Cristal Arco-Íris`;
}

async function loadLegalDocument(language) {
  const documentName = legalRoot?.dataset.document;
  const documentContent = document.querySelector("#document-content");
  if (!documentName || !documentContent) return;

  try {
    const response = await fetch(`data/${documentName}.json`, { cache: "no-cache" });
    if (!response.ok) throw new Error("Document data was unavailable.");
    loadedDocument = await response.json();
    renderLegalDocument(language);
  } catch (_error) {
    documentContent.replaceChildren();
    appendTextElement(
      documentContent,
      "p",
      "Não foi possível carregar este documento. Tente novamente mais tarde.",
      "error-copy"
    );
  }
}

async function changeLanguage(requestedLanguage) {
  const language = setActiveLanguage(requestedLanguage);
  if (legalRoot) {
    if (loadedDocument) renderLegalDocument(language);
    else await loadLegalDocument(language);
  } else {
    renderHome(language);
  }
}

languageButtons.forEach((button) => {
  button.addEventListener("click", () => changeLanguage(button.dataset.language));
});

changeLanguage(FALLBACK_LANGUAGE);
