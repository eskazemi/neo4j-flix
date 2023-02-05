from uuid import UUID
from src.core.utils import get_time
from typing import (
    List,
    Dict
)
from src.core.provider.filters_neo import CONDITIONS_MAP


class NeoClineDriver:

    @staticmethod
    def __create_node(tx, node_name: str, data: dict):
        prefix = node_name[0].lower()
        node_name = node_name.capitalize()

        k_v_pairs = [f"{key}: ${key}" for key in data.keys()]
        values = []
        for pair in k_v_pairs:
            values.append(f"{pair}")
        query = f"""
        MERGE ({prefix}:{node_name}
        { {" ,".join(values)} } 
        ) RETURN {prefix}""".replace("'", "")
        result = tx.run(query, **data)
        return result

    @staticmethod
    def __create_relation(tx, node_1_label: str, relationship_type: str, node_2_label: str,
                          where: Dict = None, property_key=None, property_value=None):
        node_1_prefix = node_1_label[0].lower()
        node_2_prefix = node_2_label[0].lower()
        node_1_label = node_1_label.capitalize()
        node_2_label = node_2_label.capitalize()

        if property_value:
            query = ("MATCH (%s: $node_1_label), "
                     "(%s: $node_2_label) "
                     "MERGE (%s)-[: %s {%s: $property_value}]->(%s)"
                     % (node_1_prefix,
                        node_2_prefix,
                        node_1_prefix,
                        relationship_type,
                        property_key,
                        node_2_prefix,
                        ))
            tx.run(query,
                   node_1_label=node_1_label,
                   node_2_label=node_2_label,
                   property_value=property_value)
            result = tx.run(query)
            return result
        elif where:
            query = f"""
            MATCH ({node_1_prefix}:{node_1_label}), ({node_2_prefix}:{node_2_label})
            WHERE {node_1_prefix}.{where["key"]} {where["condition"]} {node_2_prefix}.{where["value"]} 
            MERGE ({node_1_prefix})-[r:{relationship_type.upper()}]->({node_2_prefix})
            """
            result = tx.run(query)
            return result
        else:
            query = f"""
            MATCH ({node_1_prefix}:{node_1_label}), ({node_2_prefix}:{node_2_label})
            MERGE ({node_1_prefix})-[r:{relationship_type.upper()}]->({node_2_prefix})
            """
            result = tx.run(query)
            return result

    @staticmethod
    def __query_node_id(tx, node_label, node_name):
        query = ("MATCH (a: %s { name: $node_name }) "
                 "RETURN id(a) AS node_id"
                 % node_label)
        result = tx.run(query, node_name=node_name)
        record = result.single()
        return record["node_id"]

    @staticmethod
    def __create_property_for_node(tx, node_id, node_label, property_key,
                                   property_value):
        query = ("MATCH (a: %s) "
                 "WHERE id(a) = $id "
                 "SET a.%s = $property_value"
                 % (node_label,
                    property_key))
        tx.run(query, id=node_id, property_value=property_value)

    @staticmethod
    def __filter(tx, node_name: str, key: str, condition: str, value: str):
        condition_val = CONDITIONS_MAP.get(condition, "=")
        prefix = node_name[0].lower()
        node_name = node_name.capitalize()
        query = (
            f"MATCH ({prefix}:{node_name}) "
            f"WHERE {prefix}.{key} {condition_val} ${value} "
            f"RETURN {prefix}"
        )
        result = tx.run(query, **{key: value})
        return [record for record in result]

    @staticmethod
    def __find_all(tx, node_name: str):
        prefix = node_name[0].lower()
        node_name = node_name.capitalize()
        query = (
            f"MATCH ({prefix}:{node_name}) WHERE n.deleted_at IS NULL RETURN {prefix}"
        )
        result = tx.run(query)
        return [record for record in result]



    @staticmethod
    def __delete_soft_delete_node(tx, node_id, time: get_time()):
        query = (
                    "MATCH (n:node) .... SET n.deleted_at %s"
                ) % time

        tx.run(query)

    @staticmethod
    def __delete_node(tx, node_id):
        query = ()

        tx.run(query)

    @staticmethod
    def __delete_all_nodes(tx):
        query = (
            "MATCH (n) DETACH DELETE n"
        )

        tx.run(query)

    # -----------------------------------------------------------------------
    @classmethod
    async def create_node(cls, session_factory, node: str, data: dict,):
        """
        create node
        """

        with session_factory() as session:
            session.write_transaction(cls.__create_node, node, data)



    @classmethod
    async def query_node_id(cls, session_factory, node_label, node_name):
        with session_factory() as session:
            node_id = session.read_transaction(cls.__query_node_id, node_label,
                                               node_name)
        return node_id

    @classmethod
    async def create_property_for_node(cls, session_factory, node_label,
                                       node_name,
                                       property_dict):
        """

        """

        with session_factory as session:
            node_id = session.write_transaction(cls.__query_node_id,
                                                node_label, node_name)
            for k, v in property_dict.items():
                session.write_transaction(cls.__create_property_for_node,
                                          node_id, node_label, k, v)

    @classmethod
    async def create_relation(cls, session_factory, node_1: str,
                                  relation: str,
                                  node_2: str,
                                  where: Dict=None,
                                property_dict: dict =None
                                ):

        if not property_dict:
            with session_factory() as session:
                session.write_transaction(cls.__create_relation,
                                          node_1,
                                          node_2,
                                          relation,
                                          where,
                                          )
        else:
            for k, v in property_dict.items():
                with session_factory() as session:
                    session.write_transaction(
                        cls.__create_relation,
                        node_1,
                        node_2,
                        relation,
                        where,
                        k,
                        v,
                        )

    # --------------------------------get -------------------------------------

    @classmethod
    async def select_all(cls, session_factory, node: str,
                         limit: int = None, after: int = None):
        with session_factory() as session:
            result = session.read_transaction(cls.__find_all, node)
        return result


    # ------------------------------- delete ----------------------------------
    @classmethod
    async def soft_deleter_node(cls, session_factory, query: dict | UUID,
                                node: str):
        """
        Updates data in collection
        """
        pass

    @classmethod
    def delete_all_nodes(cls, session_factory):
        with  session_factory() as session:
            session.write_transaction(cls.__delete_all_nodes)
        print("All nodes and relationships deleted")


    # -----------------------------filter-------------------------------------

    @classmethod
    async def filter(cls, session_factory, node: str, key: str,
                         condition: str,
                         value: str) -> List:
        """

        """
        with session_factory() as session:
            result = session.read_transaction(cls.__filter, node, key,
                                              condition, value)
            return result








    # def retrieve_node_by_label_and_id(self, label: str, id_value: int) -> {}:
    #     """
    #     Return the record corresponding to a Neo4j node identified by the given label, and by
    #     an "id" attribute with a value as specified,
    #     within the context of the given session
    #     TODO: add a version that looks up the value of a single field
    #     EXAMPLE:
    #         record = conn.retrieve_node_by_id("patient", 123)
    #         gender = record["gender"]
    #     :param label:       A string with a Neo4j label
    #     :param id_value:    An integer with a value to match an attribute named "id" in the nodes
    #     :return:            A dictionary with the record information (the node's attribute names are the keys), if found;
    #                         if not found, return None
    #     """
    #
    #     sess = self.get_session()       # Retrieve or create a "session" object
    #
    #     cypher = "MATCH (n:%s {id:$id}) RETURN n" % label   # Construct the Cypher string
    #     #print("In retrieve_node_by_label_and_id(). Cypher: " + cypher)
    #
    #     result_obj = sess.run(cypher, id=id_value)   # A new neo4j.Result object
    #     # Alternate way:
    #     # result_obj = sess.run(cypher, {"id" : id})
    #
    #     record = result_obj.single()

        # if record is None:
        #     return None
        #
        # node = record[0]
        # return node