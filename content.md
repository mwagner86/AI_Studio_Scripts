## 4. Netzwerkforensik

Die **Netzwerkforensik** sucht relevante Spuren in *vorher aufgezeichneter* digitaler Kommunikation zwischen Geräten.
In dieser Lerneinheit erfahren Sie, wie man relevante Kommunikation in **Netzwerkmitschnitten** aufzeichnet und diese später nach verschiedenen Aspekten analysiert.

> [!faq] **Verständnisfrage**
> Man kann die Kommunikation auch in Echtzeit analysieren, ohne sie vorher aufzuzeichnen.
>
> Warum ist dieses Vorgehen für forensische Zwecke ungeeignet?
> Wofür kann man es sinnvoll einsetzen?
>
> > [!NOTE]- Antwort
> > Ohne Aufzeichnung hat man kein Beweismaterial und die Ergebnisse sind nicht reproduzierbar.
> > Zudem sind komplexere Analysen ohne Speicherung der Kommunikation kaum möglich.
> >
> > Echtzeit-Analysen werden z.B. in Firewalls und zur Erkennung/Verhinderung von Angriffen eingesetzt (*Intrusion Detection and Prevention Systems*).

### 4.1. Netzwerkmitschnitte

> [!info] **Definition**
> In einem **Netzwerkmitschnitt** (*network capture / packet capture*) wird digitale Kommunikation zwischen Geräten zur späteren Auswertung ganz oder auszugsweise persistent gespeichert.

Jedes aufgezeichnete Datenpaket wird mit einem **Zeitstempel** und einem Längenfeld versehen.
Hinzu kommen (je nach Format) Metadaten für den gesamten Netzwerkmitschnitt, z.B. die Zeitzone oder die verwendete Netzwerktechnologie.

Um die Integrität der Spuren zu gewährleisten, dürfen Netzwerkmitschnitte *nur durch passives Mithören* erstellt werden, ohne aktiv in die Übertragung einzugreifen.

> [!example]
> Hacking-Techniken wie [ARP Spoofing](https://en.wikipedia.org/wiki/ARP_spoofing) oder [MAC flooding](https://en.wikipedia.org/wiki/MAC_flooding) dürfen also nicht bei der Erstellung von Netzwerkmitschnitten eingesetzt werden.

#### Umfang der Aufzeichnung

*In der Netzwerkforensik kann man nur untersuchen, was vorher aufgezeichnet wurde.*

Man muss also vorab — oft lange bevor ein Anlass für eine forensische Untersuchung vorliegt — entscheiden, **welche Kommunikation wann, wo und in welchem Detailgrad** aufgezeichnet werden soll.

> [!faq] **Verständnisfrage**
> Aus forensischer Sicht wäre es ideal, *ständig die gesamte Kommunikation* "auf Vorrat" aufzuzeichnen. Warum ist dies normalerweise nicht praktikabel?
>
> > [!NOTE]- Antwort
> > * Sehr hoher Speicherbedarf und -kosten
> > * Performance-Verluste im Netzwerk, wenn die Aufzeichnung einen Engpass darstellt
> > * Vorschriften zu Datenschutz und Privatsphäre können verletzt werden
> > * Die aufgezeichneten Daten sind ggf. auch für Angreifer interessant und stellen ein zusätzliches Sicherheitsrisiko dar

Bei der Erstellung von Netzwerkmitschnitten muss man also Kompromisse eingehen.
Eine **praktische Strategie** könnte aus zwei Komponenten bestehen:

* *Permanent "auf Vorrat"* zeichnet man nur einen sehr kleinen Teil der Kommunikation auf, den man für forensisch besonders wertvoll hält, z.B. externe Verbindungen zu einem speziell geschützten Netzsegment.
* *Anlassbezogen* wird kurzzeitig gezielt mehr aufgezeichnet, z.B. aller Traffic von/zu einem bestimmten Server, auf den man einen laufenden Angriff erkennt oder vermutet.

---

**Wie detailliert** soll die Kommunikation aufgezeichnet werden?
Die wesentliche Entscheidung ist, ob für jede Übertragungseinheit (Frame, Paket, Segment, …)

* *nur Metadaten* wie Zeitstempel, Paketheader, Größe
* oder *der komplette Inhalt*

aufgezeichnet werden soll.

Die Aufzeichnung nur von Metadaten benötigt viel weniger Platz und genügt für viele Analysen.
Inhalte sollte man nur aufzeichnen, wenn man sie auch sinnvoll auswerten kann, z.B. bei unverschlüsselten Anwendungsprotokollen.

#### Datenschutzaspekte

Bei der Erstellung und Speicherung von Netzwerkmitschnitten müssen die anwendbaren Datenschutzvorschriften beachtet werden.

> [!quote]
> Personenbezogene Daten müssen … dem Zweck angemessen und erheblich sowie auf das für die Zwecke der Verarbeitung notwendige Maß beschränkt sein ("Datenminimierung").
>
> — DSGVO Art. 5

Der Begriff "personenbezogene Daten" wird heute recht weit ausgelegt:

> [!IMPORTANT]
> Schon IP- oder MAC-Adressen stellen personenbezogene Daten dar, wenn das benutzte Gerät einer Person zugeordnet werden kann, z.B. ein privater Internet-Anschluss oder der feste Arbeitsplatz-PC einer Mitarbeiterin.

Netzwerkmitschnitte sollten daher nur in angemessenem Umfang erstellt werden.
Sie sind zeitnah zu löschen, sobald sie nicht mehr benötigt werden.

### 4.2. Aufzeichnung

Netzwerkmitschnitte werden an einer ausgewählten **logischen Netzwerkschnittstelle** (*logical network interface*) des betreffenden Rechners aufgezeichnet.
Diese wird vom Netzwerk-Subsystem des Betriebssystems zur Verfügung gestellt und repräsentiert

* eine **physische** Netzwerkschnittstelle (*physical interface*) wie Ethernet oder WLAN oder
* eine vom Betriebssystem bereitgestellte **virtuelle** Netzwerkschnittstelle (z.B. Loopback, Bridge).

> [!example]
> Welche logischen Netzwerkschnittstellen hat ihre Parrot-VM, welche das zugehörige Hostsystem?
> Finden Sie heraus, was diese Interfaces jeweils repräsentieren.

Die Aufzeichnung erfolgt mit einem geeigneten Tool in der Regel auf Layer 2 (z.B. Ethernet-Frames) oder Layer 3 (z.B. IP-Pakete) des Protokoll-Stacks.

> [!WARNING]
> Bei Aufzeichnung auf einer bestimmten Schicht sind nur die Daten ab dieser Schicht aufwärts verfügbar, z.B. gehen bei Aufzeichnung auf Layer 3 (IP) die Header der Ethernet-Frames verloren, in denen die IP-Pakete verpackt sind.

Um die Datenmenge schon bei der Aufzeichnung zu reduzieren, bieten die meisten Tools Möglichkeiten zur gezielten Filterung der aufzuzeichnenden Kommunikation (*capture filters*), z.B. nach Quell-/Ziel-Adressen, Ports oder Protokollen.

> [!quote]
> Der aufzeichnende Prozess greift auf "Rohdaten" der betreffenden Netzwerkschnittstelle zu.
> Dafür benötigt er normalerweise erhöhte Privilegien, z.B. unter Linux die *Capabilities* `CAP_NET_RAW` und `CAP_NET_ADMIN`.

Zur Speicherung von Netzwerkmitschnitten gibt es verschiedene **Dateiformate**.
Die meisten Open-Source-Tools unterstützen [PCAP](https://ietf-opsawg-wg.github.io/draft-ietf-opsawg-pcap/draft-ietf-opsawg-pcap.html) (*packet capture*) bzw. dessen Nachfolger [PCAP Next Generation (pcapng)](https://ietf-opsawg-wg.github.io/draft-ietf-opsawg-pcap/draft-ietf-opsawg-pcapng.html).

> [!NOTE] 📖 **Pflichtlektüre**
> Lesen Sie die Artikel [What is a PCAP file?](https://www.netresec.com/?page=Blog&month=2022-10&post=What-is-a-PCAP-file) und
> [PcapNG File Format](https://pcapng.com/).

Bei großen Datenmengen werden Netzwerkmitschnitte manchmal auch in einer Datenbank gespeichert und zur effizienten Suche indexiert.

#### Sichtbarkeit

An einer Schnittstelle kann man natürlich nur Kommunikation aufzeichnen, die dort **sichtbar** ist und prinzipiell empfangen werden kann.
Welcher Datenverkehr an einer Schnittstelle sichtbar ist, hängt von der Übertragungstechnologie und der Netzwerkstruktur ab.

Ethernet- und WLAN-Schnittstellen sind standardmäßig so konfiguriert, dass sie auf Layer 2 nur Frames empfangen, die an die eigene MAC-Adresse (oder als Broadcast) geschickt werden.
Andere Frames werden ignoriert.

Dieses für Netzwerkmitschnitte unerwünschte Verhalten kann man bei Ethernet-Schnittstellen ändern, indem man sie temporär in den [***promiscuous mode***](https://en.wikipedia.org/wiki/Promiscuous_mode) versetzt.
Dann werden alle Frames unabhängig von der Ziel-MAC-Adresse akzeptiert.

> [!WARNING]
> Der *promiscuous mode* kann theoretisch auch auf vielen WLAN-Schnittstellen aktiviert werden, funktioniert dort aber selten korrekt.

Heutige Ethernet-Netzwerke sind in der Regel *fully switched*:
Jedes Endgerät ist alleine an einen Switch-Port angeschlossen und erhält vom Switch auf Layer 2 nur die für es (individuell oder als Broadcast) bestimmten Frames.

Eine Aufzeichnung an der Endgeräte-Schnittstelle enthält dann nur den Traffic von/zu diesem Endgerät.
Der *promiscuous mode* ist hier wirkungslos.

Will man in einem *fully switched network* gleichzeitig den Datenverkehr mehrerer Endgeräte aufzeichnen, muss dies an einem geeigneten Switch oder Router erfolgen.
Oft kann man dort einen Port als **Monitoring Port** konfigurieren, auf den alle den Switch/Router passierenden Frames automatisch kopiert werden.

Am Monitoring Port schließt man dann einen Rechner an, mit dem der Netzwerkmitschnitt erstellt wird.
Manche (teurere) Router/Switches bieten integrierte Möglichkeiten zur Aufnahme von Netzwerkmitschnitten, sodass man keinen separaten Rechner mehr dafür benötigt.

> [!TIP]
> Wenn Sie in einem Netzwerkmitschnitt nicht die erwartete Kommunikation sehen:
> Prüfen Sie zuerst, ob Sie die richtige Schnittstelle ausgewählt haben.
> Überlegen Sie dann, ob der gesuchte Traffic an dieser Schnittstelle überhaupt sichtbar ist.

#### Zuverlässigkeit

Netzwerkmitschnitte sind normalerweise recht zuverlässig.
Trotzdem können einzelne Frames/Pakete aus technischen Gründen verloren gehen oder verfälscht werden, z.B. durch

* Kollisionen oder andere Störungen der Signale, wenn die Aufzeichnung nicht an einem der Endpunkte der Kommunikation erfolgt
* bei hoher Auslastung vollen Puffer der Schnittstelle, an der aufgezeichnet wird
* einen überlasteten Monitoring-Port an einem Switch/Router (*dropped frames*)

> [!IMPORTANT]
> Die **Vollständigkeit** und **Korrektheit** eines Netzwerkmitschnitts sind **nicht garantiert**.
> Berücksichtigen Sie diese Möglichkeit bei der forensischen Auswertung.
> Beachten Sie insbesondere fehlerhafte CRCs/Prüfsummen oder inkonsistente Sequenznummern.

> [!faq] **Verständnisfrage**
> Das TCP-Protokoll erkennt verlorene Segmente und sendet sie erneut.
> Warum können in einem Netzwerkmitschnitt trotzdem einzelne TCP-Segmente fehlen?
>
> > [!NOTE]- Antwort
> > Die Bestätigung erfolgt durch den jeweiligen Empfänger über die Sequenznummer in der ACK-Nachricht.
> > Der Netzwerkmitschnitt wird hingegen von einem passiv mithörenden Prozess erstellt, der keine Möglichkeit hat, eine Wiederholung anzufordern.

### 4.3. Tools

In diesem Abschnitt gehen wir kurz auf einige bekannte Open-Source Tools zur Aufzeichnung und Analyse von Netzwerkverkehr ein.

* [Wireshark](https://www.wireshark.org/) kennen Sie vielleicht schon aus anderen Modulen:
Ein weit verbreitetes, sehr mächtiges und komfortables Tool zur Aufzeichnung und Untersuchung von Netzwerkmitschnitten.
Für Linux/Unix, Windows und macOS verfügbar.
* [tshark](https://www.wireshark.org/docs/man-pages/tshark.html): Kommandozeilen-Variante von Wireshark mit reduziertem Funktionsumfang.
* [tcpdump](https://www.tcpdump.org/):
Vielseitiges Linux/Unix Kommandozeilen-Tool zur Aufzeichnung und Analyse von Netzwerkverkehr; einfacher und schlanker als tshark und (anders als der Name suggeriert) nicht auf TCP beschränkt.
Oft zum Netzwerk-Debugging auf Servern oder Cloud-Instanzen verwendet.
> [!TIP]
> tcpdump kann PCAP-Dateien schreiben, die man später auf einem anderen Rechner im Detail auswerten kann, z.B. mit Wireshark.
* [Arkime](https://arkime.com/): ermöglicht die effiziente Aufzeichnung, Indexierung und Auswertung von großen Mengen an Netzwerkdaten.

> [!NOTE] 📺 **Video**
> Sehen Sie das Video [Network Forensics: Tools of the Trade… at Scale and on a Budget](https://www.youtube.com/watch?v=UNQ8XwyAiBs) an.

In den Übungen werden Sie vorwiegend Wireshark und tcpdump verwenden.

Neben solchen Software-Tools gibt es auch spezialisierte Hardware-Geräte zur Aufzeichnung von Netzwerkmitschnitten, sogenannte **packet capture appliances**.

> [!example]
> Recherchieren Sie online nach solchen Geräten.
> Was ist ein typischer Funktionsumfang?
> Welche Vor- und Nachteile gegenüber rein softwarebasierten Lösungen sehen Sie?

### 4.4. Drahtlose Kommunikation

Mitschnitte drahtloser Kommunikation nimmt man am besten an einem der beteiligten Endpunkte über die zugehörige logische Schnittstelle auf:

* Bei Infrastruktur-Netzwerken wie WLAN am betreffenden Access Point (AP) / Router
* Bei Punkt-zu-Punkt-Verbindungen wie Bluetooth auf einem der beiden Geräte

Dieses Vorgehen hat den Vorteil, dass man keine speziellen Tools benötigt und sich nicht mit Details der Funkübertragung und ggf. deren Verschlüsselung befassen muss.

> [!quote]
> Falls zur Funkübertragung ein verschlüsselndes Protokoll (z.B. WPA2 bei WLAN) genutzt wird, erfolgt die Ver-/Entschlüsselung transparent durch die Hardware und die jeweiligen Treiber.
> Am logischen Netzwerk-Interface werden die Pakete im Klartext bereitgestellt.

Es hat aber auch zwei wichtige Nachteile:

* Man erhält *nur die übertragenen Datenpakete* (zum Teil mit "fake" Layer 2-Headern), aber nicht die Management- und Steuerungsnachrichten des drahtlosen Netzwerks.
* Bei Infrastruktur-Netzwerken ist die *Kommunikation zwischen Clients* im selben Netzwerk normalerweise am logischen Interface des Access Points *nicht sichtbar*.

Wenn diese Nachteile nicht akzeptabel sind, kann man *Sniffing* einsetzen:

#### Sniffing

> [!info] **Definition**
> **Sniffing** ist das Abhören und ggf. Aufzeichnen drahtloser digitaler Kommunikation durch direktes Empfangen und Decodieren der Funksignale.

Dazu benötigt man einen geeigneten Empfänger und zum Übertragungsprotokoll passende Software.
Bekannte **Open-Source Sniffing-Tools** sind [aircrack-ng](https://www.aircrack-ng.org/) und [Kismet](https://www.kismetwireless.net/).

Zum **WLAN-Sniffing** kann man einen WLAN-Adapter in den **monitor mode** versetzen, falls dessen Hard- und Firmware dies unterstützt.
In diesem Modus hört der Adapter passiv den gesamten Verkehr (incl. Management- und Steuerungspakete) auf einem selektierten Kanal mit, ohne sich selbst an einem Access Point anzumelden.

Das Paket aircrack-ng enthält das Tool [airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng), das einen WLAN-Adapter in den *monitor mode* versetzt und dem Betriebssystem als logisches Interface präsentiert.
An diesem kann man dann z.B. mit Wireshark einen Netzwerkmitschnitt erstellen.

> [!NOTE] 📖 **Pflichtlektüre**
> Lesen Sie jetzt die Anleitung https://wiki.wireshark.org/CaptureSetup/WLAN und
> die [Dokumentation zu airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng).

> [!quote]
> **Kann man ein verschlüsseltes WLAN sniffen?**
>
> Das hängt vom verwendeten Verschlüsselungsprotokoll ab.
> Wir geben hier nur eine vereinfachte kurze Zusammenfassung:
>
> Zunächst muss man das Passwort kennen oder "cracken" (darauf gehen wir hier nicht weiter ein).
>
> * WEP (veraltet, unsicher):
> wer das Passwort kennt, kann den gesamten Traffic mithören.
> * WPA2-PSK:
> jeder Client erhält einen individuellen *session key*.
> Nur wenn man den initialen Handshake zwischen Client und AP mithört, kann man daraus mit dem Passwort den session key berechnen und dann den weiteren Traffic dieses Clients entschlüsseln.
> * WPA2-Enterprise und WPA3:
> Passwort und mitgehörter Handshake reichen nicht.
> Sniffing ist nur mit Kooperation des Clients oder des AP möglich, da zur Entschlüsselung der im Handshake zwischen beiden Seiten ausgetauschte PMK (Pairwise Master Key) benötigt wird.
> Daher lohnt sich Sniffing hier nur selten.

Sniffing ist primär eine Angriffstechnik, kann aber auch forensisch nützlich sein, z.B. zur

* Suche nach kompromittierten/verdächtigen Stationen in einem WLAN
* Untersuchung der Bluetooth-Kommunikation zwischen (Embedded-) Geräten, auf deren "Innenleben" man schlecht zugreifen kann.

### 4.5. Metadaten-Analyse

Der erste (und bei verschlüsselten Inhalten einzig mögliche) Analyseschritt der Netzwerkforensik ist die **Auswertung von Metadaten**
mit dem Ziel, **verdächtige Übertragungen und Teilnehmer zu finden** (und andererseits unverdächtige auszuschließen).

Ein Netzwerkmitschnitt enthält typischerweise für jedes Paket [^7] folgende Metadaten:

1.  Zeitstempel
2.  Aufgezeichnete Länge des Pakets
3.  Header-Informationen, z.B. Ethernet-, IP-, TCP-Header, Prüfsummen.
    Im Normalfall sind geschachtelte Header aus verschiedenen Schichten vorhanden, z.B.
    hat ein über Ethernet übertragenes TCP-Segment einen Ethernet-Header, einen IP-Header und einen TCP-Header.

Aus diesen Metadaten kann man viele wertvolle Informationen ableiten, insbesondere

* zeitlich-logische Beziehungen zwischen verschiedenen Paketen herstellen und sie zu **Verbindungen** (*connections* oder allgemeiner *conversations*) zusammenfassen.
> [!quote]
> Bei TCP ist die Verbindung als Bestandteil des Protokolls klar definiert.
> Bei verbindungslosen Protokollen wie UDP verwendet man ähnlich wie bei Firewalls **Heuristiken**, die zeitnah zwischen zwei Endpunkten (z.B. IP-Adresse und Port) gesendete Pakete als Verbindung interpretieren — sich darin aber irren können!
* eine **Zeitlinie** ableiten: welcher Endpunkt (meist IP-Adresse + Port) hat wann/wie lange mit welchem anderen über welches Protokoll kommuniziert und welche Datenmenge wurde dabei in jede Richtung übertragen?
* **Verkehrsstatistiken** erstellen, z.B. zur Aktivität von Endpunkten, Verbindungen, Protokolle, Datenmengen, Paketlängen, Antwortzeiten.
* bestimmte **Angriffe erkennen**, z.B. ARP-Spoofing, Exfiltration großer Datenmengen
* manchmal durch Detailanalyse der Header und Antwortzeiten sogar Hinweise auf eingesetzte **Betriebssysteme und Anwendungssoftware** erhalten.

> [!example]
> Wireshark zeigt die Metadaten zu jedem Paket übersichtlich und strukturiert an und bietet viele Filter- und Analysefunktionen, z.B.:
>
> * Flexible Filterung der Anzeige nach Endpunkten, Protokollen etc.
> * Färben einer Verbindung: View › Colorize Conversation
> * Viele statistische Auswertungen: Statistics

### 4.6. Inhalts-Analyse

Neben den Metadaten kann man auch die **Inhalte (Nutzdaten) der Kommunikation** analysieren, *wenn diese unverschlüsselt vorliegen*.

Bei der **generischen Analyse** sucht man in den "rohen" Paketinhalten nach Textmustern, bestimmten Dateiformaten (z.B. Bilddateien) oder anderen direkt auswertbaren Informationen.
Das ist sehr einfach, da man weder spezielle Tools noch detaillierte Kenntnisse des verwendeten Anwendungsprotokolls benötigt.

Die generische Analyse ist vor allem für *textbasierte, leicht menschlich lesbare Anwendungsprotokolle* wie HTTP oder SMTP praktikabel.

> [!example]
> In Wireshark kann man über den Menüpunkt Analyze › Follow › TCP Stream den bidirektionalen Datenstrom einer TCP-Verbindung ansehen, abspeichern und darin suchen (→ [Dokumentation](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html)).

Komfortabler und effizienter ist eine **protokollspezifische Analyse**:
Eine spezielle Analysesoftware interpretiert die Protokollnachrichten mit einem dafür entwickelten Parser, extrahiert relevante Informationen und stellt diese benutzerfreundlich dar.

So können auch komplexe und binär codierte Anwendungsprotokolle gut analysiert werden.

> [!example]
> Wireshark nennt diese protokollspezifischen Analysekomponenten *dissectors* und stellt ein [API dafür](https://www.wireshark.org/docs/wsdg_html_chunked/ChapterDissection.html) bereit.
>
> Recherchieren Sie, welche *dissectors* standardmäßig in Wireshark verfügbar sind.

### 4.7. Verschlüsselte Kommunikation

Ein großer Teil der Kommunikation in heutigen Rechnernetzen ist verschlüsselt, z.B. mit den Protokollen TLS (https etc.), SSH, oder einem VPN-Protokoll.

Bei Protokollen mit moderner Verschlüsselung hat man keinen Einblick in die übertragenen Inhalte.
Nur der Beginn des Verbindungsaufbaus (**Handshake**) ist unverschlüsselt.

Ohne Kenntnis des dazugehörigen geheimen Schlüssels ist eine Entschlüsselung *nicht praktikabel*, und man kann nur die Metadaten der Verbindung forensisch auswerten.

> [!quote]
> In Netzwerkmitschnitten zeichnet man oft nur die Metadaten verschlüsselter Verbindungen auf, da man deren Inhalte sowieso nicht analysieren kann.
> Das spart viel Speicherplatz.

#### TLS umgehen/entschlüsseln

In einigen speziellen Szenarien kann man "schummeln" und die eigentlich sichere Verschlüsselung *mit Kooperation eines der Endpunkte* umgehen oder nachträglich entschlüsseln.

Wir beschreiben hier die wichtigsten Möglichkeiten für TLS:

* Oft wird serverseitig ein **Reverse Proxy mit TLS-Terminierung** verwendet.
Dieser baut meistens eine unverschlüsselte Verbindung zum Backend-Server auf, die im Klartext aufgezeichnet und analysiert werden kann.
Man sieht im Backend aber nicht mehr die Originaldaten auf TCP/IP-Ebene.
* Bis TLS 1.2 ließen sich aufgezeichnete Verbindungen mit dem **privaten Schlüssel des Server-Zertifikats** nachträglich entschlüsseln.
Ab TLS 1.3 ist dies nicht mehr möglich (*perfect forward secrecy*).
Heute wird aber oft noch TLS 1.2 verwendet.
* Wenn der Client oder der Server die im Handshake ausgetauschten *symmetrischen session keys* protokolliert, lässt sich die Verbindung damit nachträglich entschlüsseln, auch bei TLS 1.3.
Einige Browser bieten zum Debugging eine entsprechende Option (SSLKEYLOGFILE).

> [!NOTE] 📖 **Pflichtlektüre**
> Lesen Sie dazu https://wiki.wireshark.org/TLS.

#### Man-In-The-Middle-Proxy

Ausgehende TLS-Verbindungen kann man abhören, indem man sie über einen **Man-In-The-Middle-Proxy** umleitet.
Dieser arbeitet wie folgt:

1.  Der Client baut eine TLS-Verbindung zum MITM-Proxy auf.
2.  Der Proxy gibt sich im Handshake gegenüber dem Client mit einem ad hoc gefälschten Serverzertifikat als der gewünschte Server aus.
3.  Gleichzeitig baut der Proxy eine neue TLS-Verbindung zum "echten" Server auf.
4.  Jetzt sitzt der Proxy "in der Mitte" zwischen beiden Verbindungen und kann die gesamte Kommunikation zwischen Client und Server im Klartext aufnehmen, ggf. modifizieren, und weiterleiten.

Damit dieser Ansatz funktioniert, muss auf jedem Client

* ein **gefälschtes Root-Zertifikat** installiert sein, mit dem der Proxy seine gefälschten Zertifikate signiert, und
* alle ausgehenden TLS-Verbindungen über den Proxy geleitet werden (durch Proxy-Konfiguration oder entsprechendes IP-Routing).

> [!quote]
> In der Netzwerkforensik kann ein MITM-Proxy gezielt eingesetzt werden, um die ausgehende TLS-Kommunikation eines (unbekannten) Programms zu analysieren, z.B. auf einem mobilen oder IoT-Gerät.
> Ein bekanntes Open-Source-Tool ist [mitmproxy](https://mitmproxy.org/).

Manche Unternehmen leiten permanent alle ausgehenden TLS-Verbindungen über einen MITM-Proxy, um diese untersuchen zu können.
Dies ist aus forensischer Sicht hilfreich, andererseits aber sehr riskant:

> [!IMPORTANT]
> Mit einem MITM-Proxy verliert man die Ende-zu-Ende-Verschlüsselung.
> Der Proxy selbst und der dort im Klartext aufgezeichnete Traffic sind attraktive Angriffsziele und stellen ein erhebliches neues Sicherheitsrisiko dar.
> Daher sollte ein solcher Proxy allenfalls temporär und gezielt eingesetzt werden.

### 4.8. Zusammenfassung

* Die Netzwerkforensik sucht relevante Spuren in vorher aufgezeichneter digitaler Kommunikation, sogenannten Netzwerkmitschnitten.
Dazu muss man vorab festlegen, was aufgezeichnet werden soll.
* Die Aufzeichnung erfolgt meist an einer logischen Netzwerkschnittstelle.
Welche Kommunikation dort sichtbar ist, hängt von der Übertragungstechnologie und der Netzwerkstruktur ab.
* Viele Switches/Router bieten einen Monitoring-Modus, der den gesamten Traffic zur Aufzeichnung an einen bestimmten Port kopiert.
* Drahtlose Kommunikation kann man an den zugehörigen logischen Schnittstellen mitschneiden.
Man kann auch direkt die Funkübertragung abhören (Sniffing); bei modernen verschlüsselten Protokollen aber nur eingeschränkt mitlesen.
* Bekannte Open-Source-Tools zur Aufnahme und Analyse von Netzwerkschnittstellen sind Wireshark (mit tshark), tcpdump und Arkime.
Sie speichern Netzwerkmitschnitte als PCAP- oder PCAP-NG-Dateien.
* Durch Auswertung der aufgezeichneten Paket-Metadaten kann man Verbindungen identifizieren, eine Zeitlinie ableiten, Verkehrsstatistiken erstellen und verdächtige Übertragungen/Teilnehmer erkennen.
* Unverschlüsselte Paketinhalte kann man auch inhaltlich untersuchen.
Generische Analysen suchen in den "rohen" Inhalten direkt z.B. nach Textmustern.
Protokollspezifische Analysen interpretieren die Nachrichten des Anwendungsprotokolls und extrahieren strukturierte Informationen daraus.
* Bei Protokollen mit moderner Verschlüsselung hat man keinen Einblick in die Inhalte.
Nur mit dem dazugehörigen geheimen Schlüssel kann man die Kommunikation entschlüsseln.
In der Regel muss man dazu mit einem der Endpunkte kooperieren.

### 4.9. Übungen

#### Allgemeine Hinweise

*Diese Hinweise gelten für diese und alle künftigen Übungen.*

> [!IMPORTANT]
> **Die Ergebnisse einiger Übungen werden evtl. später in einem Moodle-Test abgefragt und bewertet.**
> Wenn eine Aufgabe einen entsprechenden Hinweis enthält, notieren Sie bitte die genauen Antworten auf betreffenden Fragen.
> Zusätzlich empfehle ich Ihnen, Ihren Lösungsweg zu protokollieren.

1.  Inputdaten sind oft als **komprimierte Dateien/Archive** gegeben.
    Diese packen Sie je nach Format (das per Konvention an der Dateiendung erkennbar ist) in der Shell mit dem passenden Befehl aus:
    * `example.gz` mit `gunzip -k example.gz` (durch die Option `-k` bleibt die komprimierte Datei erhalten)
    * `example.xz` mit `unxz -k test.xz`
    * `example.tar.gz` mit `tar xf example.tar.gz` (tar-Archiv, kann mehrere Dateien enthalten)
    * `example.zip` mit `unzip example.zip` (zip-Archiv, kann mehrere Dateien enthalten)
2.  In manchen Aufgaben sollen Sie im Stil einer [Capture the flag (CTF)](https://en.wikipedia.org/wiki/Capture_the_flag_(cybersecurity))-Challenge eine versteckte **Flag** finden.
    Flags sind ASCII-codierte Strings in einem festgelegten Format, das sie leicht erkennbar macht.
    Alle Flags in diesem Modul haben das Format `ITF{bE1spIelFlAG}` und müssen in Moodle-Tests vollständig incl. des Rahmens `ITF{}` angegeben werden.
    Flags können Buchstaben, Ziffern und Sonderzeichen enthalten.
    Sie sind immer *case sensitive*.

#### A. Netzwerkmitschnitte auf Parrot-VM und Hostsystem

In [ParrotOS](https://www.parrotsec.org/download/) ist Wireshark standardmäßig installiert.
Installieren Sie [Wireshark](https://www.wireshark.org/) auch auf dem *Hostsystem* Ihrer Parrot-VM und starten Sie dann die VM.

1.  Starten Sie mit Wireshark parallel Netzwerkmitschnitte auf dem virtuellen Ethernet-Interface Ihrer VM und dem aktiven externen Netzwerk-Interface (Ethernet oder WLAN) des Hostsystems.
2.  Testen Sie die Verbindung zwischen VM und Host von beiden Seiten mit `ping` auf die jeweilige IP-Adresse, die Sie z.B. in Linux mit dem Befehl `ip addr` herausfinden können.
    Betrachten Sie jeweils die `ping`-Anfragen und -Antworten in Wireshark auf der VM und auf dem Hostsystem.
3.  Generieren Sie Internet-Traffic (z.B. im Browser) zuerst auf der VM, dann auf dem Hostsystem.
    Betrachten Sie jeweils die Kommunikation in Wireshark auf der VM und auf dem Hostsystem.
    Vergleichen Sie beide Sichten und erklären Sie evtl. beobachtete Unterschiede.
4.  Fahren Sie die VM herunter und ändern Sie die [Netzwerkeinstellungen der VM](https://www.virtualbox.org/manual/ch06.html) so, dass jetzt *bridged networking* verwendet wird.
    Starten Sie die VM neu und wiederholen Sie Teil 1-3.
    Was hat sich geändert?
    Erklären Sie die Veränderungen.

#### B. tcpdump ausprobieren

Das vielseitige Kommandozeilen-Tool `tcpdump` ist in ParrotOS bereits installiert.
Machen Sie sich anhand der [Manpage](https://www.tcpdump.org/manpages/tcpdump.1.html) und des Tutorials [Let’s learn tcpdump!](https://wizardzines.com/zines/tcpdump/) damit vertraut.

> [!TIP]
> `tcpdump` benötigt direkten Zugriff auf die Netzwerkschnittstellen und muss daher normalerweise als `root` (oder mit `sudo`) ausgeführt werden.

Führen Sie die folgenden Aktionen mit `tcpdump` aus und geben Sie jeweils das vollständige Kommando dazu an.

1.  Einen Mitschnitt aller Pakete an der (virtuellen) Ethernet-Schnittstelle in die Datei `dump.pcap` schreiben.
    Öffnen Sie diese Datei dann mit Wireshark und prüfen Sie den Mitschnitt.
2.  `dump.pcap` nach https-Traffic (TCP Port 443) durchsuchen und die Paketheader dazu anzeigen.
3.  DNS-Anfragen auf allen Interfaces und die Antworten dazu anzeigen.
4.  ARP-Requests und Antworten dazu an der Ethernet-Schnittstelle mit MAC-Adressen anzeigen, IP-Adressen numerisch darstellen.

#### C. Netzwerkmitschnitt analysieren

Es gibt erste Hinweise darauf, dass ein bestimmter PC das Ziel eines Angriffs war und Daten daraus entwendet wurden.
Die Datei [net-capture.pcap](../dl/net-capture.pcap) enthält einen Netzwerkmitschnitt dieses PCs.

Analysieren Sie diesen mit Wireshark und suchen Sie nach Hinweisen auf mögliche Angriffe.
Beginnen Sie mit verschiedenen statistischen Auswertungen.
Sehen Sie sich dann die Metadaten und Inhalte der Verbindungen genauer an.
Achten Sie auch auf zeitliche Zusammenhänge.
Welche Kommunikation erscheint Ihnen legitim, welche verdächtig?

Beantworten Sie insbesondere folgende Fragen.

1.  Bestimmen Sie den SHA-256 Hashwert der `.pcap`-Datei (Shell-Kommando: `sha256sum`).
2.  Welche MAC-Adresse und welche IP-Adresse(n) hat der untersuchte PC?
3.  Welche DNS-Abfragen können Sie erkennen?
4.  Bei welcher Suchmaschine wurde nach welchem Begriff gesucht?
5.  Zu welchen https-Webservern (Port 443) wurden von diesem PC aus Verbindungen aufgebaut?
6.  Wie lauten die IP-Adresse und die Zugangsdaten für den FTP-Server?
    Welcher Server-Port wird für den FTP-Datenupload verwendet?
    Rekonstruieren Sie die übertragenen Daten und finden Sie die Flag darin.
    **Notieren Sie Ihre Ergebnisse zu dieser Teilaufgabe; sie werden ggf. in einem Moodle-Test abgefragt.**
7.  Welchen weiteren signifikanten Traffic erkennen Sie?
    Klassifizieren Sie die Kommunikation jeweils als verdächtig / unverdächtig / unklar.
8.  Welche IP-Adressen scheinen mit Angreifern in Verbindung zu stehen (mit Begründung)?

#### D. TLS entschlüsseln

**Notieren Sie Ihre Ergebnisse zu dieser Aufgabe, sie werden ggf. in einem Moodle-Test abgefragt.**

Das Archiv [net-tls.tar.gz](../dl/net-tls.tar.gz) enthält einen Netzwerkmitschnitt als PCAP-Datei sowie ein *keylog*, in dem der Client die geheimen *session keys* einer TLS-Verbindung protokolliert hat.

Analysieren Sie den Netzwerkmitschnitt mit Wireshark und [entschlüsseln Sie die TLS-Verbindung](https://wiki.wireshark.org/TLS).

1.  Bestimmen Sie die SHA-256 Hashwerte der `.pcap`- und `.keylog`-Datei.
2.  Welche TLS-Version wird verwendet?
3.  Wie lauten die IP-Adressen von Client und Server der TLS-Verbindung?
4.  Welche MAC-Adresse hat der Client?
5.  Welche IP-Adresse hat die erste Zwischenstation der IP-Pakete vom Client zum Server?
6.  Bis zu welchem Tag ist das TLS-Zertifikat des Servers gültig?
    Tipp: Finden Sie das Zertifikat in Wireshark im TLS-Handshake und speichern Sie es in einer Binärdatei `cert.bin` ab.
    Dann betrachten Sie den Inhalt mit dem Befehl
    `openssl x509 -in cert.bin -noout -text` (vgl. Modul *Angewandte Kryptographie*).
7.  Geben Sie die vollständige URI (beginnend mit "https://") des HTTP-Requests an.
    Welchen Teil davon können Sie im herausfinden, ohne die TLS-Übertragung zu entschlüsseln?
8.  Welcher Browser (*user agent*) wird verwendet (Name/Versionsnummer)?
9.  Finden Sie die Flag in der Antwort des Servers.

#### E. Das eigene WLAN sniffen

Sniffen Sie Ihr eigenes privates WLAN (**auf keinen Fall ein fremdes!**)
erst mit [Kismet](https://www.kismetwireless.net/), dann mit
[Wireshark](https://wiki.wireshark.org/CaptureSetup/WLAN) und [airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng).
Dazu müssen Sie diese Tools *direkt auf einem Rechner mit geeigneter WLAN-Hardware* installieren.
Eine VM ist dafür normalerweise nicht geeignet, da sie keinen direkten Zugriff auf die WLAN-Hardware hat.

1.  Welche (Teile der) Kommunikation sehen Sie jeweils und welche forensisch relevanten Informationen können Sie daraus entnehmen?
2.  Falls Ihr WLAN mit WPA2-PSK verschlüsselt ist: Versuchen Sie, den WLAN-Verkehr mit Wireshark zu entschlüsseln, siehe diese [Anleitung](https://wiki.wireshark.org/HowToDecrypt802.11).

Notieren Sie Ihre Erfahrungen für unsere Diskussion.

> [!NOTE]
> Es gibt prinzipiell auch Möglichkeiten, einer VM die direkte Kontrolle über einzelne Hardwarekomponenten wie einen WLAN-Adapter zu geben (*PCI/USB passthrough*).
> Das funktioniert aber leider nur mit mancher Hardware und ist für unser Modul zu kompliziert.

[^7]: Wir nennen hier alle mitgeschnittenen Übertragungseinheiten generisch "Pakete"; das umfasst z.B. Ethernet-Frames, IP-Pakete und TCP-Segmente.