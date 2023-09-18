
package com.soap.ws.client_jp;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the com.soap.ws.client_jp package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _SearchPublicationByTopic_QNAME = new QName("http://ws/", "searchPublicationByTopic");
    private final static QName _SearchPublicationByTopicResponse_QNAME = new QName("http://ws/", "searchPublicationByTopicResponse");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: com.soap.ws.client_jp
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link SearchPublicationByTopic }
     * 
     */
    public SearchPublicationByTopic createSearchPublicationByTopic() {
        return new SearchPublicationByTopic();
    }

    /**
     * Create an instance of {@link SearchPublicationByTopicResponse }
     * 
     */
    public SearchPublicationByTopicResponse createSearchPublicationByTopicResponse() {
        return new SearchPublicationByTopicResponse();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchPublicationByTopic }{@code >}
     * 
     * @param value
     *     Java instance representing xml element's value.
     * @return
     *     the new instance of {@link JAXBElement }{@code <}{@link SearchPublicationByTopic }{@code >}
     */
    @XmlElementDecl(namespace = "http://ws/", name = "searchPublicationByTopic")
    public JAXBElement<SearchPublicationByTopic> createSearchPublicationByTopic(SearchPublicationByTopic value) {
        return new JAXBElement<SearchPublicationByTopic>(_SearchPublicationByTopic_QNAME, SearchPublicationByTopic.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchPublicationByTopicResponse }{@code >}
     * 
     * @param value
     *     Java instance representing xml element's value.
     * @return
     *     the new instance of {@link JAXBElement }{@code <}{@link SearchPublicationByTopicResponse }{@code >}
     */
    @XmlElementDecl(namespace = "http://ws/", name = "searchPublicationByTopicResponse")
    public JAXBElement<SearchPublicationByTopicResponse> createSearchPublicationByTopicResponse(SearchPublicationByTopicResponse value) {
        return new JAXBElement<SearchPublicationByTopicResponse>(_SearchPublicationByTopicResponse_QNAME, SearchPublicationByTopicResponse.class, null, value);
    }

}
