# BuildForBharat

### Theme: Retail & Logistics

### Problem Name: Optimal storage & retrieval in m*n sparse matrix

### Requirements:

    pip install bplustree
    pip install diskcache
    pip install asyncio

### Running the code

To retrieve the list of merchants associated with a particular pincode:

    nc 34.125.204.13 3389
    GET_MERCHANT <pincode>

For other features:

    nc 34.125.204.13 8080
    
    #Add new merchant
    ADD_NEW_MERCHANT <merchant_id> <pincode1 pincode2 ...>

    #Add merchants to an existing pincode
    ADD_MERCHANTS <pincode> <number of merchants>

    #Removing a merchant
    REMOVE_MERCHANT <pincode> <merchant_id1 merchant_id2 ...>
    



### Project Goals/Objectives
1. **Establish Efficient Pincode Based Serviceability** : Develop a robust system to facilitate merchants in defining the pincodes where they can deliver products and services, ensuring retrieval of the list of serving merchants in a rapid manner.

2. **Ensure Scalability and Real-Time Verification** : Design an optimal data structure capable of storing pincode serviceability by merchants, accommodating the vast number of pincodes (30,000) and merchants (100 million), with approximately 10% enabling pincode-based serviceability.

4. **Ensure Data Integrity and Security** : Implement stringent data validation measures to ensure the accuracy and reliability of pincode serviceability information stored in the system.

### Features

1. **B+Tree Utilization**: Implemented a B+ tree data structure to map pincodes with merchants, facilitating efficient organization and retrieval of data for pincode-based serviceability.

2. **Merchant Management Features**: Integrated features for adding and removing merchants within the system, ensuring flexibility and adaptability to changing business needs and serviceability requirements.

3. **Caching mechanisms**:
   
    3.1 _Retrieval Cache_: Employed an in-memory cache to store frequently accessed data, optimizing retrieval speed and reducing latency for commonly requested information.

    3.2 *Internal Cache*: Utilized a larger in-memory cache to accommodate less frequently accessed data, enhancing overall system performance by reducing the need for disk access.

    3.3 *Disk Cache* : Implemented a cache mechanism specifically designed for managing addition and removal of merchants, allowing changes to be temporarily stored until reaching a buffer limit, after which they are flushed using multiprocessing to minimize impact on server response time.

**Benefits of caching**

*Reduced Disk Access*: By caching frequently accessed data and minimizing disk access, the system experiences improved performance and responsiveness.

*Enhanced Response Time*: The use of caching mechanisms, particularly in-memory caching, leads to faster response times for user queries and operations.

*Optimized Operations*: Caching strategies not only improve response time but also optimize operations involving merchant management, ensuring efficient utilization of system resources.


### Architecture and Design

I. Modular architecture that provides flexible integration option: 
1. **Component-Based Design**: The code employs a modular architecture with distinct components like ServerOps, BPlusTree, and WriteCache, facilitating flexible integration by encapsulating specific functionalities within each module.
2. **Separation of Concerns**: Each component focuses on a specific aspect of the system, such as data storage, server operations, or caching, ensuring clear separation of concerns and enabling independent development and integration.
3. **Defined Interfaces**: Well-defined interfaces between modules establish communication protocols and enable seamless integration, allowing developers to replace or extend components without impacting the overall system functionality.
4. **Plug-and-Play Functionality**: The modular architecture supports plug-and-play functionality, allowing developers to easily add, remove, or replace modules as needed, thus enhancing flexibility and adaptability in system design and implementation.

II. Tech evaluation would include the following:

1. **Reusability - of APIs, algorithms, data sets** : Reusability is achieved by abstracting the formats of data being stored and using B+ Trees.
2. **Extensibility - to other use-cases**: The code's modular architecture, with components like ServerOps and BPlusTree, allows for extensibility by providing clear separation of concerns and well-defined interfaces.
3. **Scalability - working at population scale with optimal capacity & minimal latency** : The code ensures scalability by employing optimized data structures like BPlusTree and caching mechanisms, enabling efficient handling of large data sets at population scale.
4. **Security - ensuring transactional guarantees** :The code enforces transactional guarantees through atomic operations and error handling mechanisms, ensuring data integrity and consistency. By utilizing techniques like locking and rollback procedures, it protects against concurrency issues and ensures that transactions are executed reliably, thereby enhancing security and preventing data corruption or loss during server operations.



### Customization and Deployment
The server is running on _google cloud_.
Connection Protocol:
*TCP*: This is the default protocol for your project's communication.
*HTTP*: The system can be customized to switch between TCP and HTTP connections based on requirements.

Data Format:
*JSON*: Data can be structured and transmitted in JSON format, enabling easy parsing and interoperability with various systems.
*Other Formats*: Customization options can be provided to support other data formats if needed.

### Important links
Link to repository: https://github.com/Shreyas529/BuildForBharat

