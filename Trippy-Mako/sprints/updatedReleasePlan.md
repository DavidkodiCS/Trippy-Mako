# Updated Release Plan

| Sprint | Duration | Start Date  | End Date    | Goals                                    | Deliverables                                     | Status     |
|--------|----------|-------------|-------------|------------------------------------------|--------------------------------------------------|------------|
| 1      | 2 weeks  | 2024-10-21  | 2024-11-03  | Set Up Python Environment                | Environment Setup for Testing and Development    | Finished   |
| 2      | 2 weeks  | 2024-11-17  | 2024-11-30  | CLI Tool Skeleton                        | Core CLI structure, basic configuration system   | Finished |
|        |          |             |             |                                          | Commands for triggering main features (TURN, Auth)|            |
|        |          |             |             |                                          | Error handling, user feedback, help command      |            |
|        |          |             |             | Subitems: Testing and Feedback of Design       |                                                  |            |
| 3      | 3 weeks  | 2024-12-01  | 2024-12-21  | Virtual Box Testing Environment Setup    | VyOS Configuration, 5 VMs and 3 Vnets Setup, Terraform | Not Started |
|        |          |             |             | Subitems: 5 VMs, 3 Vnets Manual, Terraform, VyOS |                     |            |
| 4      | 4 weeks  | 2024-12-22  | 2025-01-18  | Authentication                           | TLS and Certificates                            | Not Started |
|        |          |             |             | Subitems: TLS and Tunneling, Forge Certificates, Server and Client Certificates, Trust Anchor: OpenSSH (Python library) | | |
| 5      | 2 weeks  | 2025-01-19  | 2025-02-01  | Implement TURN Protocol (Part 1)         | Allocate Request/Response Handling, Refresh Request Handling | Not Started |
|        |          |             |             | Subitems: Sending/Receiving Allocate Requests and Responses | | |
| 6      | 2 weeks  | 2025-02-02  | 2025-02-15  | Implement TURN Protocol (Part 2)         | CreatePermission Request/Response Handling, Send Indication | Not Started |
|        |          |             |             | Subitems: Refresh Request Handling, CreatePermission Handling | | |
| 7      | 2 weeks  | 2025-02-16  | 2025-03-01  | Implement TURN Protocol (Part 3)         | ChannelBind Request/Response, Data Relaying | Not Started |
|        |          |             |             | Subitems: Send/Receive Indications, UDP Datagram Handling | | |
| 8      | 2 weeks  | 2025-03-02  | 2025-03-15  | Implement TURN Protocol (Part 4)         | ChannelData Message Handling | Not Started |
|        |          |             |             | Subitems: Formatting and Relaying ChannelData Messages | | |
| 9      | 2 weeks  | 2025-03-16  | 2025-03-29  | Merge Authentication and TURN Protocol   | Integration of Authentication and TURN Features | Not Started |
| 10     | 2 weeks  | 2025-03-30  | 2025-04-12  | CLI Tool Development                     | Basic CLI Functionality | Not Started |
| 11     | 1 week   | 2025-04-13  | 2025-04-19  | Documentation                            | Finalize Documentation from Capstone Work | Not Started |