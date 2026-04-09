import reflex as rx
from app.states.landing_state import LandingState


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.a(
            rx.el.div(
                rx.el.span(
                    "D",
                    class_name="font-['Cormorant_Garamond'] text-lg font-bold text-[#F5F0E8]",
                ),
                class_name="w-[34px] h-[34px] bg-[#1A1612] rounded-[2px] flex items-center justify-center shrink-0",
            ),
            rx.el.span(
                "DocDraft",
                class_name="font-['Cormorant_Garamond'] text-xl font-semibold text-[#1A1612] ml-2.5",
            ),
            href="#",
            class_name="flex items-center no-underline",
        ),
        rx.el.div(class_name="flex-1"),
        rx.el.ul(
            rx.el.li(
                rx.el.a(
                    "Product",
                    href="#features",
                    class_name="text-sm font-medium text-[#6B5E50] hover:text-[#1A1612] transition-colors",
                ),
                class_name="list-none",
            ),
            rx.el.li(
                rx.el.a(
                    "Solutions",
                    href="#results",
                    class_name="text-sm font-medium text-[#6B5E50] hover:text-[#1A1612] transition-colors",
                ),
                class_name="list-none",
            ),
            rx.el.li(
                rx.el.a(
                    "Pricing",
                    href="#",
                    class_name="text-sm font-medium text-[#6B5E50] hover:text-[#1A1612] transition-colors",
                ),
                class_name="list-none",
            ),
            rx.el.li(
                rx.el.a(
                    "Resources",
                    href="#",
                    class_name="text-sm font-medium text-[#6B5E50] hover:text-[#1A1612] transition-colors",
                ),
                class_name="list-none",
            ),
            class_name="hidden md:flex items-center gap-8",
        ),
        rx.el.div(class_name="hidden md:block w-8"),
        rx.el.a(
            "Request Demo",
            href="#waitlist",
            class_name="bg-[#1A1612] text-[#F5F0E8] text-sm font-semibold px-6 py-2.5 rounded-[2px] hover:bg-[#2E2820] transition-colors",
        ),
        class_name="fixed top-0 left-0 right-0 z-50 h-[72px] flex items-center px-8 md:px-16 bg-[#F5F0E8] border-b border-[#C8B89A]/20 shadow-sm",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "AI-POWERED LEGAL INTELLIGENCE",
                    class_name="text-[9px] font-semibold text-[#8B7355] border border-[#C8B89A] px-3 py-1 rounded-full tracking-[3px] mb-6 inline-block",
                ),
                rx.el.h1(
                    "Draft contracts with exceptional precision.",
                    class_name="font-['Cormorant_Garamond'] text-4xl md:text-[52px] font-medium text-[#1A1612] leading-[1.1] tracking-tight mb-6",
                ),
                rx.el.p(
                    "DocDraft automates the drafting, review, and management of legal documents. Designed for firms and legal departments that demand quality and efficiency.",
                    class_name="text-[15px] text-[#6B5E50] leading-[1.6] max-w-lg mb-8",
                ),
                rx.el.div(
                    rx.el.a(
                        "Request Free Demo",
                        href="#waitlist",
                        class_name="bg-[#1A1612] text-[#F5F0E8] font-semibold px-8 py-4 rounded-[2px] hover:bg-[#2E2820] transition-colors inline-block mr-4",
                    ),
                    rx.el.a(
                        "See How It Works →",
                        href="#features",
                        class_name="text-[#1A1612] font-semibold hover:translate-x-1 transition-transform inline-block py-4",
                    ),
                    class_name="flex flex-wrap items-center",
                ),
                rx.el.p(
                    "Trusted by over 500 legal firms in Spain and Latin America",
                    class_name="text-[11px] font-semibold text-[#9A8E80] tracking-wider uppercase mt-12",
                ),
                class_name="max-w-2xl",
            ),
            class_name="w-full md:w-[55%] flex items-center p-8 md:p-16",
        ),
        rx.el.div(
            rx.image(
                src="/legal_professional_workspace.png",
                class_name="w-full h-full object-cover",
            ),
            class_name="w-full md:w-[45%] h-[400px] md:h-auto",
        ),
        class_name="flex flex-col md:flex-row min-h-screen pt-[72px] bg-[#F5F0E8] font-['Outfit']",
    )


def trust_bar() -> rx.Component:
    return rx.el.section(
        rx.el.p(
            "USED BY THE BEST LEGAL TEAMS",
            class_name="text-[9px] font-semibold text-[#8B7355] tracking-[3px] mb-8",
        ),
        rx.el.div(
            rx.foreach(
                [
                    "Cuatrecasas",
                    "Garrigues",
                    "Uría Menéndez",
                    "Pérez-Llorca",
                    "Linklaters",
                    "Clifford Chance",
                ],
                lambda name: rx.el.span(
                    name,
                    class_name="font-['Cormorant_Garamond'] text-lg text-[#9A8E80]",
                ),
            ),
            class_name="flex flex-wrap justify-center items-center gap-x-12 gap-y-6",
        ),
        class_name="py-16 px-8 text-center bg-[#EDE8DF]",
    )


def feature_card(
    num: str, icon: str, title: str, desc: str, is_dark: bool
) -> rx.Component:
    bg_color = "bg-[#1A1612]" if is_dark else "bg-[#EDE8DF]"
    text_color = "text-[#F5F0E8]" if is_dark else "text-[#1A1612]"
    desc_color = "text-[#9A8E80]" if is_dark else "text-[#6B5E50]"
    return rx.el.div(
        rx.el.span(
            num, class_name="text-[11px] font-semibold text-[#8B7355] tracking-[2px]"
        ),
        rx.icon(icon, class_name="w-7 h-7 text-[#8B7355]"),
        rx.el.h3(
            title,
            class_name=f"font-['Cormorant_Garamond'] text-[22px] font-medium {text_color} tracking-tight leading-[1.2]",
        ),
        rx.el.p(desc, class_name=f"text-[13px] leading-[1.65] {desc_color}"),
        class_name=f"flex flex-col gap-6 p-10 md:p-12 {bg_color} transition-transform hover:-translate-y-1 duration-300",
    )


def features() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                "HOW IT WORKS",
                class_name="text-[9px] font-semibold text-[#8B7355] tracking-[3px] mb-4 block",
            ),
            rx.el.h2(
                "Everything your firm needs.",
                class_name="font-['Cormorant_Garamond'] text-[46px] font-medium text-[#1A1612] leading-none mb-4",
            ),
            rx.el.p(
                "A comprehensive platform covering the complete legal document lifecycle.",
                class_name="text-[15px] text-[#6B5E50] max-w-lg mx-auto",
            ),
            class_name="text-center mb-16",
        ),
        rx.el.div(
            feature_card(
                "01",
                "file-text",
                "Smart Drafting",
                "Leverage AI to create complex contracts using proprietary firm data and logic.",
                False,
            ),
            feature_card(
                "02",
                "brain",
                "AI Review",
                "Automated identification of risks, inconsistencies, and regulatory non-compliance.",
                True,
            ),
            feature_card(
                "03",
                "shield-check",
                "Regulatory Compliance",
                "Real-time monitoring of legal changes affecting your entire document library.",
                False,
            ),
            feature_card(
                "04",
                "users",
                "Team Collaboration",
                "Integrated workflows for secure sharing and version control within the platform.",
                True,
            ),
            feature_card(
                "05",
                "zap",
                "Instant Generation",
                "Produce complete dossiers in seconds from simple data inputs or conversation.",
                False,
            ),
            feature_card(
                "06",
                "lock",
                "Bank-Grade Security",
                "Enterprise-level encryption and private hosting for complete client confidentiality.",
                True,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-[2px]",
        ),
        id="features",
        class_name="py-24 px-8 md:px-16 bg-[#F5F0E8]",
    )


def results_stats() -> rx.Component:
    def stat_row(num: str, label: str) -> rx.Component:
        return rx.el.div(
            rx.el.span(
                num,
                class_name="font-['Cormorant_Garamond'] text-[48px] font-medium text-[#1A1612] leading-none w-24 shrink-0",
            ),
            rx.el.div(class_name="w-[1px] h-12 bg-[#C8B89A]"),
            rx.el.p(label, class_name="text-[13px] text-[#6B5E50] leading-[1.6]"),
            class_name="flex items-center gap-6",
        )

    return rx.el.section(
        rx.el.div(
            rx.image(
                src="/legal_professional_workspace.png",
                class_name="w-full h-full object-cover",
            ),
            class_name="hidden lg:block w-1/2",
        ),
        rx.el.div(
            rx.el.h2(
                "Measurable results from day one.",
                class_name="font-['Cormorant_Garamond'] text-[34px] font-medium text-[#1A1612] leading-[1.2] mb-12 max-w-sm",
            ),
            rx.el.div(
                stat_row(
                    "87%",
                    "Reduction in drafting time through AI-assisted automation and intelligent templates.",
                ),
                stat_row(
                    "3.2x",
                    "Return on investment in the first quarter of implementation for corporate departments.",
                ),
                stat_row(
                    "99.4%",
                    "Accuracy in regulatory compliance monitoring across multiple jurisdictions.",
                ),
                class_name="flex flex-col gap-10",
            ),
            class_name="w-full lg:w-1/2 p-12 md:p-20 flex flex-col justify-center bg-[#EDE8DF]",
        ),
        id="results",
        class_name="flex flex-col lg:flex-row min-h-[560px]",
    )


def comparison_table() -> rx.Component:
    def table_row(feature: str, trad: str, dd: str) -> rx.Component:
        return rx.el.tr(
            rx.el.td(feature, class_name="py-4 px-8 text-[13px] text-[#C8B89A]"),
            rx.el.td(
                trad, class_name="py-4 px-8 text-[13px] text-[#9A8E80] text-center"
            ),
            rx.el.td(
                dd,
                class_name="py-4 px-8 text-[13px] text-[#F5F0E8] font-semibold text-center",
            ),
            class_name="border-b border-[#2E2820] odd:bg-[#1E1C16] even:bg-[#242018] hover:bg-[#2A2620] transition-colors h-14",
        )

    return rx.el.section(
        rx.el.div(
            rx.el.span(
                "WHY DOCDRAFT",
                class_name="text-[9px] font-semibold text-[#7A6E62] tracking-[3px] mb-4 block",
            ),
            rx.el.h2(
                "The intelligent alternative.",
                class_name="font-['Cormorant_Garamond'] text-[46px] font-medium text-[#F5F0E8] mb-14 text-center",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "FEATURE",
                                class_name="text-[9px] font-semibold tracking-[2px] text-[#7A6E62] text-left px-8 py-4 bg-[#242018]",
                            ),
                            rx.el.th(
                                "Traditional",
                                class_name="text-xs font-medium text-[#7A6E62] bg-[#2E2820] w-[220px]",
                            ),
                            rx.el.th(
                                "DocDraft",
                                class_name="text-xs font-bold text-[#F5F0E8] bg-[#8B7355] w-[220px]",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        table_row(
                            "Contract Drafting", "4-6 hours manual", "15 min with AI"
                        ),
                        table_row(
                            "Regulatory Review",
                            "External consultants",
                            "Real-time automated",
                        ),
                        table_row(
                            "Template Management",
                            "Scattered in folders",
                            "Centralized & smart",
                        ),
                        table_row(
                            "Team Collaboration",
                            "Emails & versions",
                            "Real-time integrated",
                        ),
                        table_row(
                            "Compliance", "Annual manual audit", "Continuous monitoring"
                        ),
                        table_row("Cost per Document", "$150-400", "From $12"),
                    ),
                    class_name="w-full max-w-[900px] border-collapse mx-auto",
                ),
                class_name="w-full overflow-x-auto",
            ),
            class_name="max-w-6xl mx-auto",
        ),
        id="comparison",
        class_name="py-24 px-8 bg-[#1A1612]",
    )


def waitlist_cta() -> rx.Component:
    return rx.el.section(
        rx.el.span(
            "GET STARTED",
            class_name="text-[9px] font-semibold text-[#8B7355] tracking-[3px] mb-6 block",
        ),
        rx.el.h2(
            "Transform your legal practice.",
            class_name="font-['Cormorant_Garamond'] text-4xl md:text-[52px] font-medium text-[#1A1612] mb-4",
        ),
        rx.el.p(
            "Join leading firms already using DocDraft.",
            class_name="text-[15px] text-[#6B5E50] mb-12",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="your@email.com",
                on_change=LandingState.set_waitlist_email,
                class_name="flex-1 h-14 px-6 bg-[#F5F0E8] border border-[#C8B89A] focus:outline-none focus:border-[#8B7355] text-sm",
                default_value=LandingState.waitlist_email,
            ),
            rx.el.button(
                "Request Access",
                on_click=LandingState.submit_waitlist,
                class_name="h-14 px-10 bg-[#1A1612] text-[#F5F0E8] font-semibold hover:bg-[#2E2820] transition-colors shrink-0",
            ),
            class_name="flex flex-col md:flex-row w-full max-w-lg mx-auto mb-8",
        ),
        rx.el.div(
            rx.el.span("✓ 14-day free trial", class_name="text-xs text-[#9A8E80] mx-4"),
            rx.el.span(
                "✓ No credit card required", class_name="text-xs text-[#9A8E80] mx-4"
            ),
            class_name="flex flex-col md:flex-row justify-center gap-4",
        ),
        id="waitlist",
        class_name="py-32 px-8 text-center bg-[#EDE8DF]",
    )


def final_cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.span(
                "READY?",
                class_name="text-[9px] font-semibold text-[#7A6E62] tracking-[3px] mb-4 block",
            ),
            rx.el.h2(
                "Start drafting smarter.",
                class_name="font-['Cormorant_Garamond'] text-[46px] font-medium text-[#F5F0E8] mb-6 leading-tight",
            ),
            rx.el.p(
                "Schedule a personalized demo and discover how DocDraft can transform your firm.",
                class_name="text-[15px] text-[#9A8E80] mb-10 max-w-md",
            ),
            rx.el.a(
                "Schedule Demo",
                href="#waitlist",
                class_name="bg-[#8B7355] text-[#F5F0E8] font-semibold px-10 py-4 rounded-[2px] hover:bg-[#A88C6D] transition-colors inline-block",
            ),
            class_name="w-full lg:w-1/2 p-12 md:p-20 bg-[#1A1612] flex flex-col justify-center",
        ),
        rx.el.div(
            rx.image(
                src="/legal_professional_workspace.png",
                class_name="w-full h-full object-cover",
            ),
            class_name="hidden lg:block w-1/2",
        ),
        id="final-cta",
        class_name="flex flex-col lg:flex-row min-h-[500px]",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "D",
                        class_name="font-['Cormorant_Garamond'] text-lg font-bold text-[#F5F0E8]",
                    ),
                    class_name="w-8 h-8 bg-[#8B7355] rounded-[2px] flex items-center justify-center shrink-0",
                ),
                rx.el.span(
                    "DocDraft",
                    class_name="font-['Cormorant_Garamond'] text-lg font-semibold text-[#F5F0E8] ml-2.5",
                ),
                class_name="flex items-center mb-6",
            ),
            rx.el.p(
                "Legal intelligence for the modern firm",
                class_name="text-xs text-[#9A8E80] leading-loose",
            ),
            class_name="w-full md:w-1/4 mb-12 md:mb-0",
        ),
        rx.el.div(
            rx.el.span(
                "PRODUCT",
                class_name="text-[10px] font-semibold text-[#8B7355] tracking-[2px] mb-6 block",
            ),
            rx.el.nav(
                rx.el.a(
                    "Features",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Pricing",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Integrations",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "API",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
            ),
            class_name="w-1/2 md:w-1/4 mb-12 md:mb-0",
        ),
        rx.el.div(
            rx.el.span(
                "COMPANY",
                class_name="text-[10px] font-semibold text-[#8B7355] tracking-[2px] mb-6 block",
            ),
            rx.el.nav(
                rx.el.a(
                    "About",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Case Studies",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Legal Blog",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Contact",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
            ),
            class_name="w-1/2 md:w-1/4 mb-12 md:mb-0",
        ),
        rx.el.div(
            rx.el.span(
                "LEGAL",
                class_name="text-[10px] font-semibold text-[#8B7355] tracking-[2px] mb-6 block",
            ),
            rx.el.nav(
                rx.el.a(
                    "Privacy Policy",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "Terms of Use",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
                rx.el.a(
                    "GDPR Compliance",
                    href="#",
                    class_name="text-[13px] text-[#9A8E80] hover:text-[#F5F0E8] mb-4 block transition-colors",
                ),
            ),
            class_name="w-1/2 md:w-1/4",
        ),
        rx.el.div(class_name="w-full h-[1px] bg-[#2E2820] mt-16 mb-8"),
        rx.el.div(
            rx.el.span(
                "© 2025 DocDraft. All rights reserved.",
                class_name="text-[11px] text-[#5A5045]",
            ),
            rx.el.div(
                rx.el.a(
                    "Privacidad",
                    href="#",
                    class_name="text-[11px] text-[#5A5045] hover:text-[#9A8E80] ml-6",
                ),
                rx.el.a(
                    "Términos",
                    href="#",
                    class_name="text-[11px] text-[#5A5045] hover:text-[#9A8E80] ml-6",
                ),
                rx.el.a(
                    "Cookies",
                    href="#",
                    class_name="text-[11px] text-[#5A5045] hover:text-[#9A8E80] ml-6",
                ),
                class_name="flex",
            ),
            class_name="flex flex-col md:flex-row justify-between items-center gap-4",
        ),
        class_name="py-20 px-8 md:px-16 bg-[#1A1612] flex flex-wrap font-['Outfit']",
    )


def landing_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        hero(),
        trust_bar(),
        features(),
        results_stats(),
        comparison_table(),
        waitlist_cta(),
        final_cta(),
        footer(),
        class_name="bg-[#F5F0E8] overflow-x-hidden",
    )