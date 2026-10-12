# Pancake - Privacy Policy
## Version 2.0 — Effective Date: August 17, 2025 — Last Update: October 12, 2026

Copyright © 2026 Suited. All rights reserved.

## Preamble

This Privacy Policy ("Policy") explains how the Pancake Development Team ("Team") collects, uses, stores, protects and discloses information in connection with Pancake. It applies to the official Pancake Discord bot, the Pancake Embed Editor, the Pancake Plugin Portal, and their related websites, APIs, authentication features, documentation and infrastructure (collectively, the "Service").

These components share the official Discord OAuth application where authentication is required. However, each component processes information according to its own functionality; using the same authentication application does not mean that every type of data is automatically shared across all components.

By using the Service, you acknowledge that you have been informed of the practices described in this Policy. Where consent is required by applicable law, the Team will obtain it through an appropriate mechanism. Personal Data may otherwise be processed on another applicable legal basis, such as providing a requested feature, legitimate interests or compliance with legal obligations.

## 1. Scope and Data Controller

**1.1 Scope.** This Policy applies to data collected or processed by Pancake's official bot, Embed Editor, Plugin Portal and related infrastructure. It does not govern Discord's independent processing, third-party plugins' independent processing, or external websites and services, which are subject to their own policies.

**1.2 Responsible Party.** The Pancake Development Team operates, maintains and governs the Service.

**Legal identity of the responsible individual or entity:** [Insert the full legal name of the responsible individual or legal entity before publication.]

**Domicile or legal address:** [Insert the applicable legal address or domicile before publication.]

**Privacy contact:** pancakebot.team@gmail.com

**Support Server:** https://discord.gg/V2psxDQdhZ

The Team acts as the responsible party for Personal Data processed by the Service, except where a third-party Plugin Author or provider independently determines its own processing purposes and means, as described in this Policy.

## 2. Information We Process

The information processed depends on which component you use, the features enabled, your settings and whether you authenticate through Discord. Not every category below is collected by every component.

### 2.1 Discord Account Information and Authentication

When you authenticate through Discord OAuth, the relevant component receives the information made available through the authorization process. Depending on the component and requested scope, this may include:

- Discord user ID, username or display name, including `global_name` where available;
- Avatar or profile references;
- Temporary OAuth state, authorization and session information; and
- Authentication and security records required to establish, maintain, expire or revoke access.

The Plugin Portal uses Discord OAuth2 with the `identify` scope for account-related features. Other components may process the profile information needed for their own functionality. The precise information returned depends on Discord's API and the authorization granted.

The Service does not ask you to provide your Discord account password directly to Pancake. Authentication is handled by Discord's authorization system.

### 2.2 Discord Bot Data

When Pancake is installed in a Discord Server, the bot may process information reasonably necessary for enabled features, including:

- Discord user IDs, Server (guild) IDs, usernames, discriminator where available, avatars, roles, permissions and membership-related metadata;
- Event timestamps and information related to messages or actions;
- Messages, message fragments, attachments and URLs processed for commands, moderation, logging, evidence or other enabled features;
- Moderation records such as warnings, strikes, mutes and bans, where those features are enabled;
- Server and user configuration, including prefixes, log channels and module settings; and
- Support requests, screenshots, descriptions, contribution metadata, bug reports or other information you voluntarily provide.

Message content is retained only where necessary for the relevant enabled moderation, logging, command or evidence features. Some information, such as user IDs, usernames, avatars, roles or event metadata, may be processed even when a person does not directly interact with the bot, because the bot needs it to provide features enabled by a Server.

Pancake is designed to process only the minimum amount of information reasonably necessary to provide its features.

### 2.3 Embed Editor Data

When you use the Pancake Embed Editor, it may process or temporarily store the content needed to create, validate, preview, export or retrieve Discord embeds, including:

- Message content, titles, descriptions, fields, buttons, authors and footers;
- Images, URLs, colors, formatting and other supported embed properties;
- Generated retrieval codes and their expiration timestamps; and
- Technical or session information required to operate the editor and protect it against abuse.

Embed Data is stored to provide the editor's temporary retrieval functionality. Generated codes are identifiers for retrieving the corresponding data, not passwords, authentication credentials or security tokens. Embed Data is not routinely reviewed by the Team except where reasonably necessary for operation, security, abuse investigation or legal compliance.

### 2.4 Plugin Portal Data and Interactions

When you browse the Pancake Plugin Portal, it may process information associated with published Plugin listings and related account features, including:

- Plugins you like and Plugins you save to favorites;
- Information used to prevent duplicate or invalid interactions and maintain displayed engagement counts;
- Plugin view counts and limited usage information needed to operate listings and protect the API; and
- Public Plugin Content, such as names, descriptions, commands, categories, author display names, images, videos and external links.

Likes and favorites are separate features. Favorites help users keep track of Plugins; likes may contribute to a Plugin's displayed engagement count. View counts may be rate-limited and are not necessarily unique human visits or proof of a particular person's activity.

Plugin listings are managed by authorized Team Members. The Portal does not provide a general public submission system for users to publish or edit Plugin listings.

### 2.5 Configuration, Usage and Support Information

Depending on the component, the Service may process configuration settings, aggregated or pseudonymized usage metrics where feasible, error reports, support communications, contribution information and other data voluntarily supplied by users. Such information is used to provide features, respond to requests, maintain service reliability and investigate technical or security issues.

### 2.6 Technical and Security Information

The Service and its infrastructure may process technical information reasonably necessary to operate, diagnose and protect the Service, including request timestamps, browser or user-agent information, connection metadata, error logs and security logs.

The Embed Editor or Plugin Portal and their infrastructure may process IP addresses or portions thereof where reasonably necessary for delivery, security, diagnostics or abuse prevention. This does not mean that every component collects or stores IP addresses in its own database. The Pancake Discord bot does not collect client IP addresses by default. The extent and retention of technical information may depend on the hosting, networking and infrastructure providers involved.

### 2.7 Administrative Information

For authorized administration of the Plugin Portal or related systems, the Service may process administrative Discord identifiers, authorization records, permission information and other records needed to validate administrative actions. Where an administrative authentication system uses credentials or password hashes, these are subject to separate server-side controls and are not intended to be stored in the public frontend's persistent storage.

### 2.8 Information Not Intentionally Requested

The Service does not request your Discord account password. The Plugin Portal does not request a Discord bot token for ordinary sign-in. The Service is not designed to collect sensitive personal information, payment-card data or financial account information for its ordinary functionality. Do not submit such information unless an official, separately documented feature expressly requires it.

## 3. Purposes and Legal Bases for Processing

The Team may process information for the following purposes, where applicable:

- **Providing the Service:** operating bot commands, moderation and logging features, configuring Servers, creating and retrieving embeds, displaying Plugin listings, and maintaining likes and favorites;
- **Authentication and account management:** establishing, maintaining, expiring and revoking authenticated sessions and validating permissions;
- **Security and abuse prevention:** detecting fraud, unauthorized access, excessive automated requests, malicious activity and other attempts to compromise the Service;
- **Support and troubleshooting:** responding to user inquiries, investigating incidents, diagnosing errors and maintaining reliability;
- **Improvement and analytics:** understanding aggregated or pseudonymized feature usage and improving compatibility or performance where feasible; and
- **Legal compliance:** responding to lawful requests and meeting applicable legal obligations.

Depending on the applicable law and the activity involved, the legal basis may include providing a requested service, legitimate interests, compliance with legal obligations or consent where required. Where processing depends on consent, you may withdraw it as permitted by law; withdrawal does not invalidate processing that was lawful before withdrawal or require retention periods that are otherwise legally necessary to be disregarded.

The Team does not sell Personal Data or intend to use it for unrelated targeted advertising or profiling.

## 4. Discord Authentication, Cookies and Sessions

Authentication for connected components is provided through the official Discord OAuth application where required. The Service receives only the information made available through the relevant authorization process and does not receive your Discord password.

The web components may use limited authentication technologies, including temporary HTTP-only cookies, short-lived authorization codes, access tokens, session information and browser `sessionStorage`, as required by their authentication design. These mechanisms are used to establish and protect authenticated sessions, not for advertising. The Plugin Portal's current implementation uses a temporary HTTP-only cookie during OAuth, exchanges a short-lived one-use authorization code for an access token, stores a hash of issued access tokens on the backend, and maintains the active token in browser session storage during the authenticated session.

Sessions or credentials may expire automatically. Where logout functionality is available, it may revoke the active access token when the request succeeds. Logging out does not necessarily delete separate account records, such as likes or favorites. Disabling cookies or browser storage may prevent some functions from operating correctly.

Discord may independently process information under its own terms and privacy policy.

## 5. User Content and Third-Party Plugins

Users remain responsible for content and data they submit, generate, configure or share through the Service and should provide only information they have the legal right to use.

The Team does not claim ownership of user-submitted Embed Data. The Embed Editor does not routinely review generated content, but the Team may access or process it where reasonably necessary to operate or secure the Service, investigate abuse or comply with law.

Third-party Plugins may collect or process additional information when enabled in a Server. Plugin Authors are independently responsible for their own Plugins and their data practices to the extent they determine those practices. Users and Server administrators should review available Plugin documentation and privacy policies before enabling a Plugin. A Plugin's presence in the Portal or an official distribution does not mean that the Team has independently audited or verified all of its data practices.

## 6. Data Sharing and Third-Party Providers

The Team does not sell Personal Data or share it for third-party advertising purposes. Information may be processed or disclosed when reasonably necessary to provide the Service, including in the following circumstances:

**Service providers.** Depending on the component and current infrastructure, providers may include hosting, database, backup, CDN, networking and infrastructure services, such as GitHub Pages, Render, MongoDB Atlas, Railway or other providers used to operate Pancake. These providers may process information needed to deliver, store, secure or maintain the relevant component, subject to their own terms and applicable obligations.

**Discord.** Discord provides the platform, OAuth authorization and related functionality. Its independent processing is governed by Discord's own policies.

**External content.** The Service may link to or embed external media, images, documentation, repositories or other websites. When your browser accesses that content, the relevant third party may receive technical information, potentially including your IP address and request metadata.

**Plugins.** Third-party Plugins may process data independently as described in Section 5.

**Legal and safety reasons.** The Team may disclose information where reasonably necessary to comply with applicable law or lawful requests, protect rights or security, investigate abuse or fraud, or prevent imminent harm.

The Team does not control the independent privacy or security practices of third-party providers, Plugins or external websites. Their respective terms and privacy policies apply to their processing.

## 7. Data Retention and Deletion

Information is retained only for as long as reasonably necessary for the purposes described in this Policy, subject to feature settings, operational requirements, security needs, technical limitations and applicable law. Retention differs by component and data category:

- **Bot logs and moderation records:** the default retention period is **90 days**, unless Server administrators configure another period or an enabled Plugin defines a different policy. Other bot data may be retained as necessary for the relevant feature.
- **Embed Data:** stored temporarily and may be deleted automatically upon expiration, after manual deletion, during maintenance, to investigate abuse, for security reasons or when required by law. Generated codes and their associated data are not guaranteed to remain available for any particular period. The Embed Editor is not a permanent storage, archival or backup service.
- **Authentication data:** session and authentication information is subject to expiration and revocation mechanisms. Technical or security records may be retained for a reasonable period needed to protect or maintain the Service.
- **Portal likes and favorites:** account-related interactions may remain stored while needed to provide these features, unless removed or otherwise deleted.
- **Plugin listings:** published records and related content may remain available while maintained by authorized Team Members.
- **Support, backup and operational information:** may be retained longer where reasonably necessary for troubleshooting, security, fraud prevention, legal compliance or recovery. The Team does not promise immediate removal from every backup, provider log or infrastructure system when a record is deleted.

The Team may delete or anonymize information where reasonably practicable once it is no longer needed. Valid deletion requests will be handled to the extent reasonably possible, subject to legal obligations, the rights of others, security requirements and technical limitations.

## 8. Data Security and Incident Response

The Team implements reasonable technical and organizational measures intended to protect information against unauthorized access, disclosure, alteration, loss or destruction. Depending on the component, measures may include access controls, server-side authorization checks, protected session handling, token expiration and revocation, storage of token hashes rather than raw access tokens, encrypted transport (TLS where applicable), and encryption at rest where supported by the underlying infrastructure.

No website, network, authentication system, database or electronic storage or transmission method can guarantee absolute security.

Please report suspected vulnerabilities or security incidents promptly and privately to **pancakebot.team@gmail.com**, preferably including reproduction steps and a suitable contact method. Users should avoid public disclosure until the Team has had a reasonable opportunity to investigate and mitigate the issue. The Team will make reasonable efforts to investigate and remediate confirmed issues. Where required by law or otherwise feasible, affected parties will be notified and reasonable remediation steps will be taken.

## 9. Your Privacy Rights and Requests

Depending on your jurisdiction, you may have rights concerning Personal Data, including the right to request access, rectification, deletion or cancellation, objection to or restriction of processing, and data portability where applicable. Under Mexican law, applicable rights may include the **ARCO rights**: access, rectification, cancellation and opposition.

To submit a request, email **pancakebot.team@gmail.com** with the subject line **"Privacy Request — Pancake"**. Please describe the request and relevant data, and provide your Discord user ID or other information reasonably needed to locate the records and verify your identity. Do not send your Discord password, access token or other authentication secrets.

The Team may request additional information where reasonably necessary to verify identity, clarify the request or locate relevant records. Requests will be reviewed under applicable law. A request may be limited or denied where a legal obligation, legitimate security need, third-party right, technical limitation or other lawful exception applies; where appropriate, the Team will explain the limitation.

You may remove individual likes or favorites through the relevant functionality where available. Such actions affect those interactions but do not necessarily delete all Personal Data associated with your use of the Service. Stopping use of Pancake or logging out also does not automatically delete previously stored information.

## 10. Children's Privacy

The Service is not intended for individuals who do not meet the minimum age requirements applicable to Discord and the use of the relevant Pancake component. If the Team becomes aware that Personal Data has been processed in circumstances requiring action under applicable law, it will review the matter and take reasonable steps in accordance with its legal obligations. Parents or legal representatives may contact **pancakebot.team@gmail.com** to raise a concern or request review.

## 11. International Data Processing

The Service may rely on providers whose systems, personnel or infrastructure are located outside Mexico. Accordingly, information may be processed or stored in jurisdictions other than the one from which you access the Service. Where applicable law imposes requirements on international transfers or disclosures, the Team will take the steps required by that law. Third-party providers' own international data practices are governed by their respective policies.

## 12. Service Discontinuation and Transfer of Control

If the Team intends to discontinue the Service or transfer its operation, it will make reasonable efforts, where practical, to provide notice and either transfer information to a successor with appropriate safeguards or securely decommission hosted systems. In a merger, acquisition, reorganization or similar transaction, information may be transferred to a successor operator subject to applicable law and this Policy or a substantially equivalent policy.

If the Service is discontinued without a successor, the Team will make reasonable efforts to securely delete hosted Personal Data that is no longer required for legal or operational purposes. When a person leaves the Team, that person's access to systems and data will be revoked as appropriate. Changes in Team membership do not by themselves change the purposes for which the Service processes information.

## 13. Changes to This Policy

The Team may update this Policy to reflect changes in the Service, its data practices, infrastructure, third-party providers or applicable law. Updated versions will be published through an official Pancake channel and will identify the version number, Effective Date and Last Update date as appropriate.

Material changes will be communicated through an appropriate channel where required by applicable law. Where a change introduces processing that requires additional consent, the Team will obtain that consent as necessary. Continued use of the Service does not override any consent requirement or other legal right that applies to you.

## 14. Contact

For privacy questions, requests concerning Personal Data, security concerns or legal notices, contact:

**Pancake Development Team**

Email: pancakebot.team@gmail.com

Support Server: https://discord.gg/V2psxDQdhZ

**By using any part of Pancake, you acknowledge that you have been informed of this Privacy Policy.**
